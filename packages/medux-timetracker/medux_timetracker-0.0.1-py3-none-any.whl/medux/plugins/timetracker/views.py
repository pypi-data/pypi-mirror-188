import locale
import calendar

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse
from django.utils.timezone import datetime, timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    FormView,
)
from django.utils.translation import gettext_lazy as _

from medux.common.api.interfaces import ModalFormViewMixin
from medux.common.htmx.mixins import HtmxResponseMixin, HtmxDeleteView
from medux.common.tools import monthdelta
from medux.employees.models import WorkSchedule
from medux.plugins.timetracker.forms import TimeEntryForm, LogoutWithTimeTrackingForm
from medux.plugins.timetracker.models import Holiday, HolidayStatus, TimeEntry
from medux.plugins.timetracker import calendars
from medux.core.models import User
from medux import notifications
from medux.common.api.http import HttpResponseEmpty, HttpResponseHXRedirect


class CalendarContextMixin:
    """Adds calendar data to the context.
    Arguments:
        year: the year to create context data from. If not present, the current year is taken
        month: the month to create context data from. If not present, the current month is taken
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        year = kwargs.get("year", now.year)
        month = kwargs.get("month", now.month)
        first_day = datetime(year, month, 1)
        last_day = monthdelta(first_day, 1) - timedelta(days=1)
        prev_month = monthdelta(first_day, -1)
        next_month = monthdelta(first_day, 1)
        current_month = now.month
        current_year = now.year
        context.update(
            {
                "year": year,
                "month": month,
                "first_day": first_day,
                "last_day": last_day,
                "month_label": _(first_day.strftime("%B")),
                "prev_month": prev_month,
                "next_month": next_month,
                "prev_year": year - 1,
                "next_year": year + 1,
                "current_month": current_month,
                "current_year": current_year,
            }
        )
        return context


class HolidaysView(PermissionRequiredMixin, CalendarContextMixin, TemplateView):
    template_name = "timetracker/holidays.html"
    permission_required = "timetracker.view_holiday"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = Holiday.objects.filter(
            employee__tenant=self.request.user.tenant
        ).order_by("employee_id")
        # FIXME: add firstweekday, locale as parameters
        # noinspection PyTypeChecker
        cal = calendars.HolidayCalendar(
            employee=self.request.user,
            queryset=queryset,
            firstweekday=1,
        )
        context["calendar"] = mark_safe(
            cal.formatyear(self.request.user, context["year"])
        )
        return context


class OverView(PermissionRequiredMixin, CalendarContextMixin, TemplateView):
    template_name = "timetracker/overview.html"

    def has_permission(self):
        user = self.request.user
        return user.is_authenticated and user.has_perm("timetracker.view_timeentry")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate a calendar
        now = timezone.now()
        month = context["month"] or now.month
        year = context["year"] or now.year

        cal = calendar.Calendar(firstweekday=0).itermonthdates(year=year, month=month)
        # context["calendar"] = cal.monthdatescalendar(context["year"], context["month"])
        return context


class ToggleHolidayView(HtmxResponseMixin, PermissionRequiredMixin, TemplateView):
    template_name = "timetracker/day.html"
    object: Holiday | None = None
    queryset = None

    def get_queryset(self, **kwargs):
        if self.queryset:
            return self.queryset
        self.queryset = Holiday.objects.filter(
            employee__tenant=self.request.user.tenant
        ).order_by("employee_id")
        return self.queryset

    def has_permission(self):
        user: User = self.request.user
        return user.is_employee and user.has_perm("timetracker.change_holiday")

    def get_context_data(self, year, month, day, **kwargs):
        context = super().get_context_data(**kwargs)
        thedate = timezone.datetime(year, month, day)
        queryset = self.get_queryset()
        try:
            self.object = queryset.get(employee_id=self.request.user.id, day=thedate)
            context["object"] = self.object
        except Holiday.DoesNotExist:
            pass
        context.update(
            calendars.get_holiday_context_from_day(
                employee=self.request.user.employee,
                thedate=thedate,
                queryset=queryset,
                locale=locale.getdefaultlocale(),
            )
        )
        context["day"] = thedate
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**self.kwargs)
        if self.object:
            if self.object.status == HolidayStatus.APPROVED:
                notifications.warning(
                    self.request.user, _("Holiday was already approved.")
                )
                return HttpResponseEmpty()
            elif self.object.status == HolidayStatus.NEW:
                pass
            self.object.delete()
            self.object = None
            del context["object"]
        else:
            # there is no holiday marked on this day
            self.object = Holiday.objects.create(
                employee_id=self.request.user.id, day=context["day"], type_id=1
            )
            context["object"] = self.object

        return self.render_to_response(context)


class AdminView(PermissionRequiredMixin, CalendarContextMixin, TemplateView):
    template_name = "timetracker/admin.html"

    def has_permission(self):
        return self.request.user.has_perm("timetracker.administer_holiday")


class PendingHolidayRequestsView(PermissionRequiredMixin, ListView):
    """Shows all pending holiday requests from employees in a list."""

    template_name = "timetracker/pending_holiday_list.html"
    permission_required = "timetracker.administer_holiday"
    model = Holiday

    def get_queryset(self):
        return Holiday.objects.filter(
            employee__tenant=self.request.user.tenant, status=HolidayStatus.NEW
        ).order_by("day")


class HolidaySetStatusView(HtmxResponseMixin, PermissionRequiredMixin, DetailView):
    """Sets status (approved, declined,...) of the given Holiday."""

    def get_queryset(self):
        return Holiday.objects.filter(
            employee__tenant=self.request.user.tenant, status=HolidayStatus.NEW
        ).order_by("day")

    def has_permission(self):
        user: User = self.request.user
        return (
            user.has_perm("timetracker.change_holiday")
            and self.get_object().employee.tenant == user.tenant
        )

    def post(self, request, status: str, **kwargs):
        obj = self.get_object()
        obj.status = HolidayStatus(status)
        obj.save()
        return HttpResponse()


class DeleteHolidayView(PermissionRequiredMixin, HtmxDeleteView):
    model = Holiday

    def has_permission(self):
        user = self.request.user
        # only allow deleting own holidays, or if user has "administer" perm
        return user.has_perm("timetracker.delete_holiday") and (
            user.id == self.get_object().employee.id
            or user.has_perm("timetracker.administer_holiday")
        )

    def get_queryset(self):
        return Holiday.objects.filter(
            employee__tenant=self.request.user.tenant,
            status__in=[
                HolidayStatus.APPROVED,
                HolidayStatus.NEW,
                HolidayStatus.DECLINED,
            ],
        ).order_by("day")


class TimeEntryListView(PermissionRequiredMixin, ListView):
    model = TimeEntry
    permission_required = "timetracker.view_timeentry"
    template_name = "timetracker/timeentry_list.html"

    def get_queryset(self):
        user = self.request.user
        if not user.is_employee:
            messages.error(
                self.request, _("Time entries are only available for employees.")
            )
            return TimeEntry.objects.none()
        employee = user.employee
        if not employee.active_work_schedule:
            messages.warning(
                self.request,
                _("You haven't created a work schedule yet. Please create one."),
                extra_tags="alert-dismissible",
            )
        return TimeEntry.objects.filter(
            employee=employee, work_schedule=employee.active_work_schedule
        ).order_by("-start")


class TimeEntryCreateView(ModalFormViewMixin, CreateView):
    model = TimeEntry
    form_class = TimeEntryForm
    modal_title = _("Add new time entry")
    success_event = "medux:timeentry:changed"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"employee": self.request.user.employee})
        return kwargs


class TimeEntryUpdateView(ModalFormViewMixin, PermissionRequiredMixin, UpdateView):
    model = TimeEntry
    form_class = TimeEntryForm
    modal_title = _("Edit time entry")
    success_event = "medux:timeentry:changed"

    def has_permission(self):
        # TODO: maybe require timetracker.change|add_timeentry permission here?
        return self.request.user.is_employee

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"employee": self.request.user.employee, "instance": self.get_object()}
        )
        return kwargs


class CurrentWorkScheduleView(HtmxResponseMixin, PermissionRequiredMixin, DetailView):
    model = WorkSchedule
    template_name = "timetracker/work_schedule_detail.html"

    def has_permission(self):
        user = self.request.user
        return user.is_authenticated and user.is_employee

    def get_queryset(self):
        return self.model.objects.filter(employee=self.request.user.employee)

    def get_object(self, queryset=None):
        if not self.kwargs.get("pk", None):
            return WorkSchedule.get_active(self.request.user.employee)
        return super().get_object(queryset)


class TimeEntryDeleteView(PermissionRequiredMixin, HtmxDeleteView):
    model = TimeEntry
    success_event = "medux:timeentry:changed"

    def has_permission(self):
        user = self.request.user
        return (
            user.is_employee
            and user.has_perm("timetracker.delete_timeentry")
            and self.get_object().employee == user.employee
        )


class LogoutWithTimeTrackingView(TimeEntryUpdateView):
    """A modal form view that allows finishing a time entry before logging out."""

    template_name = "timetracker/logout_with_timetracking_form.html"
    modal_title = _("Logout with time tracking")
    model = TimeEntry

    def get_queryset(self):
        return self.model.objects.filter(employee=self.request.user.employee)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        try:
            # first, try to get open time entry
            return queryset.get(end=None)
        except TimeEntry.DoesNotExist:
            # if no open time entry exists, create new one.
            work_schedule: WorkSchedule = (
                self.request.user.employee.active_work_schedule
            )
            if not work_schedule:
                return None
            weekday = timezone.localdate().weekday()
            start = work_schedule.working_hours.filter(weekday=weekday)
            if not start.exists():
                # no WTR defined for today's weekday
                return None

            return TimeEntry(
                employee=self.request.user.employee,
                work_schedule=work_schedule,
                start=start.first(),
            )

    def get_form(self, form_class=None):
        employee = self.request.user.employee
        try:
            instance = TimeEntry.objects.get(employee=employee, end=None)
        except TimeEntry.DoesNotExist:
            instance = None
        form = LogoutWithTimeTrackingForm(
            data=self.request.POST or None, instance=instance, employee=employee
        )
        return form

    def form_valid(self, form):
        # save the time entry
        super().form_valid(form)
        # and log user out.
        logout(self.request)
        return HttpResponseHXRedirect(redirect_to=settings.LOGIN_URL)

    def form_invalid(self, form):
        print(
            "form.errors:",
            form.errors,
            "\nform._errors:",
            form._errors,
            "\nself.non_field_errors:",
            form.non_field_errors(),
        )
        return super().form_invalid(form)

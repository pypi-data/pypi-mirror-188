from django.urls import reverse, reverse_lazy

from medux.common.api.interfaces import IMenuItem
from django.utils.translation import gettext_lazy as _

from medux.plugins.timetracker.models import TimeEntry


# def has_unfinished_timeentry(request):
#     """returns True if user is employee and has unfinished time slots"""
#     if request.user.is_anonymous or not request.user.is_employee:
#         return False
#     return TimeEntry.objects.filter(employee=request.user.employee, end=None).exists()


class TimetrackerDashboard(IMenuItem):
    menu = "views"
    title = _("Time tracker")
    icon = "calendar-range"
    url = reverse("timetracker:overview")


class Overview(IMenuItem):
    menu = "timetracker"
    title = _("Overview")
    icon = "house"
    separator = True
    url = reverse("timetracker:overview")


class TimeEntryList(IMenuItem):
    menu = "timetracker"
    title = _("Time entries")
    icon = "clock"
    url = reverse("timetracker:timeentry-list")


class Holidays(IMenuItem):
    menu = "timetracker"
    title = _("Holidays")
    icon = "airplane"
    url = reverse("timetracker:current-holidays")


class LogoutWithTimeTracking(IMenuItem):
    menu = "user"
    title = _("Logout with time tracking")
    url = "#"
    # url = reverse_lazy("timetracker:logout")
    weight = 90
    icon = "box-arrow-right"
    attrs = {"hx-get": reverse_lazy("timetracker:logout"), "hx-target": "#dialog"}


class Administration(IMenuItem):
    menu = "timetracker"
    title = _("Administration")
    icon = "gear"
    url = reverse("timetracker:admin")
    required_permissions = "timetracker.administer_holiday"

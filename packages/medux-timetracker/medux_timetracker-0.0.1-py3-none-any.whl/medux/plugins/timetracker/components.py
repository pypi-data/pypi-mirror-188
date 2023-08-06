from datetime import datetime, timedelta

from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from medux import notifications
from medux.common.api.interfaces import ILoginViewExtension, ILoginFormExtension
from medux.common.bootstrap import RadioSelectButtonsGroup
from .bootstrap import TimeSelector
from medux.common.tools import round_down_time

from medux.employees.models import Employee
from medux.plugins.timetracker.models import TimeEntry

COME_GO_CHOICES = (
    ("come", _("Coming")),
    ("go", _("Going")),
)


def get_rounded_time():
    """helper function to get current time, rounded down to the next unit."""
    return round_down_time(timezone.localtime(), 15).strftime("%H:%M")


class TimetrackerLoginFormExtension(ILoginFormExtension):
    """Provides simplified start/end time fields at the login form."""

    class Media:
        js = ("timetracker/js/timeselector.js",)

    field_names = ["log_time", "come_go"]

    def alter_fields(self, fields: dict):
        """add log_time and come/go fields to Login dialog"""
        fields["log_time"] = forms.TimeField(
            label=_("Login time"),
            required=False,
            initial=get_rounded_time,
        )
        fields["come_go"] = forms.ChoiceField(
            label=False, required=False, choices=COME_GO_CHOICES
        )

    def alter_layout(self, layout: Layout):
        """insert a timeselector and come/go fields into layout"""
        fields: list = layout.fields[0].fields
        fields.insert(
            2,
            Row(
                Column(
                    TimeSelector("log_time"),
                    RadioSelectButtonsGroup("come_go"),
                ),
            ),
        )

    def clean(self, cleaned_data) -> dict:
        if not cleaned_data["come_go"] in ["come", "go"]:
            return cleaned_data
        employee = Employee.objects.get(username=cleaned_data["username"])
        open_time_entry = TimeEntry.objects.filter(
            employee=employee,
            work_schedule=employee.active_work_schedule,
            end=None,
        )
        if cleaned_data["come_go"] == "come":
            if open_time_entry.exists():
                raise ValidationError(
                    _(
                        f"You already seem to have an active time entry at "
                        f"{open_time_entry.last().start.strftime('%d.%m.%Y %H:%m')}. "
                        f"Please finish this first.",
                    ),
                    code="invalid",
                )
        elif cleaned_data["come_go"] == "go":
            if open_time_entry.exists():
                if len(open_time_entry) != 1:
                    raise ValidationError(
                        _(
                            "There are more than one unfinished time entries. Please contact your administrator."
                        ),
                        code="invalid",
                    )
                else:
                    open_time_entry = open_time_entry.first()
                    today = datetime.date(datetime.today())
                    timestamp = timezone.make_aware(
                        datetime.combine(today, cleaned_data["log_time"])
                    )
                    if timestamp < open_time_entry.start:
                        raise ValidationError(
                            _(
                                f"End time ({timestamp}) cannot be before start time ({open_time_entry})."
                            ),
                            code="invalid",
                        )
        return cleaned_data


class TimetrackerLoginViewExtension(ILoginViewExtension):
    def form_valid(self, form, response) -> None:
        """After successfully logging in, save some timetracker data."""
        if not form.cleaned_data["come_go"]:
            return
        today = datetime.date(datetime.today())
        try:
            employee = Employee.objects.get(username=form.cleaned_data["username"])
            timestamp = timezone.make_aware(
                datetime.combine(today, form.cleaned_data["log_time"])
            )
            open_time_entry = TimeEntry.objects.filter(
                employee=employee, work_schedule=employee.active_work_schedule, end=None
            )
            if form.cleaned_data["come_go"] == "come":
                # TODO: make sure employee has an active_work_schedule!
                TimeEntry.objects.create(employee=employee, start=timestamp)
            elif form.cleaned_data["come_go"] == "go":
                if open_time_entry.exists():
                    open_time_entry = open_time_entry[0]
                    if open_time_entry.start < timestamp:
                        open_time_entry.end = timestamp
                        open_time_entry.save()
                    else:
                        notifications.error(
                            _("End time cannot be before start time"),
                            recipient=employee,
                        )  # TODO

        except Employee.DoesNotExist:
            pass

import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.formats import time_format
from django.utils.translation import gettext as _

from medux.common.tools import round_down_time, round_up_time
from medux.plugins.timetracker.bootstrap import TimeSelector
from medux.plugins.timetracker.models import TimeEntry


class TimeEntryForm(ModelForm):
    class Meta:
        model = TimeEntry
        fields = ["date", "start_time", "end_time", "comment"]

    class Media:
        js = ("timetracker/js/timeselector.js",)

    date = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField(required=False)

    def __init__(self, **kwargs):
        self.employee = kwargs.pop("employee")
        super().__init__(**kwargs)
        if self.instance.id:
            self.fields["date"].initial = timezone.localdate(self.instance.start)
            self.fields["start_time"].initial = time_format(
                timezone.localtime(self.instance.start)
            )
            self.fields["end_time"].initial = time_format(
                timezone.localtime(self.instance.end)
            )
        else:
            self.fields["date"].initial = timezone.localtime().date()

            self.fields["start_time"].initial = time_format(
                round_down_time(timezone.localtime(self.instance.start), 15)
            )
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "date",
            TimeSelector("start_time"),
            TimeSelector("end_time"),
            "comment",
        )

    def clean(self):
        assert self.employee.active_work_schedule
        self.cleaned_data["employee"] = self.employee
        if not "end_time" in self.cleaned_data and TimeEntry.objects.filter(
            employee=self.employee, end=None
        ):
            self.add_error(
                "end_time",
                ValidationError(
                    _(
                        "There can only be one open time entry. Please close the open one first."
                    ),
                    code="invalid",
                ),
            )
        return super().clean()

    def clean_end_time(self):
        end_time = self.cleaned_data.get("end_time", None)
        start_time = self.cleaned_data.get("start_time", None)
        if end_time:
            if end_time <= start_time:
                self.add_error(
                    "end_time",
                    ValidationError(
                        _("End time cannot be before start time."), code="invalid"
                    ),
                )
        return end_time

    def save(self, commit=True):
        instance: TimeEntry = self.instance
        instance.start = timezone.make_aware(
            datetime.datetime.combine(
                self.cleaned_data["date"], self.cleaned_data["start_time"]
            )
        )
        if self.cleaned_data["end_time"]:
            instance.end = timezone.make_aware(
                datetime.datetime.combine(
                    self.cleaned_data["date"], self.cleaned_data["end_time"]
                )
            )
        instance.employee = self.employee
        # if new TimeEntry was created, set work_schedule to default
        if not instance.id:
            instance.work_schedule = self.employee.active_work_schedule
        return super().save(commit)


class LogoutWithTimeTrackingForm(TimeEntryForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields["end_time"].required = True
        self.fields["end_time"].initial = time_format(
            round_up_time(timezone.localtime(), 15)
        )

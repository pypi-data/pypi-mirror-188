from datetime import timedelta, datetime

import django
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import TextChoices
from django.utils import timezone
from django.utils.formats import time_format, date_format
from django.utils.translation import gettext_lazy as _

from medux.employees.models import Employee, WorkSchedule, WorkingTimeRange


def _roundTime(dt: datetime = None, dateDelta: timedelta = timedelta(minutes=1)):
    """Round a datetime object to a multiple of a timedelta

    @param dt: datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
            Christian González 2020 - adjustments and small improvements
    """
    roundTo = dateDelta.total_seconds()

    if dt is None:
        dt = django.utils.timezone.now()
    # Make sure dt and datetime.min have the same timezone
    tzmin = dt.min.replace(tzinfo=dt.tzinfo)

    seconds = (dt - tzmin).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)


# class ScheduleEntry(models.Model):
#     """Entry of a roster which is a plan for working hours."""
#
#     schedule = models.ForeignKey(WorkSchedule, on_delete=models.CASCADE)
#     day = models.CharField(max_length=2, choices=DaysOfWeek.choices)
#     start = models.TimeField()
#     end = models.TimeField()
#     comment = models.CharField(max_length=255, blank=True)
#
#     def __str__(self):
#         return f"{self.day} {self.start} - {self.end}"


class TimeEntryManager(models.Manager):
    def create(self, **kwargs):
        """Set work_schedule to employee's active one if not provided."""
        if not "work_schedule" in kwargs:
            kwargs["work_schedule"] = kwargs["employee"].active_work_schedule
        return super().create(**kwargs)


class TimeEntry(models.Model):
    """A time entry for a specific block of time, of one person."""

    # TODO: Schedules must not overlap
    # TODO: time entries of one user must not overlap
    # validate time entries:
    #   TODO: start ! >= end

    objects = TimeEntryManager()

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work_schedule = models.ForeignKey(WorkSchedule, on_delete=models.PROTECT)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(
        max_length=255, blank=True, help_text=_("Optional comment for this time entry")
    )
    cached_delta = models.DurationField(_("Delta"), blank=True, null=True)

    def duration(self) -> timedelta:
        """Returns the duration of the time entry as timedelta"""
        if self.end:
            return self.end - self.start
        assert timezone.is_aware(self.start)  # DEBUG
        return timezone.localtime() - self.start

    def duration_h(self) -> float:
        return self.duration().seconds / 60 / 60

    def __str__(self):
        if self.end:
            end = time_format(timezone.localtime(self.end).time())
        else:
            end = _("now")
        return f"{self.employee}: {time_format(timezone.localtime(self.start).time())} - {end}"


    def save(self, **kwargs):
        # FIXME: rounding is dependent on current tenant, hence must be done in view.
        #     if PreferencesRegistry.get["ROUND"]:
        #         round = settings.TIMETRACKER["ROUND"]
        #         self.start = _roundTime(self.start, timedelta(minutes=round))
        #         if self.end:
        #             self.end = _roundTime(self.end, timedelta(minutes=round))
        #

        self.delta(recalculate=True)
        super().save(**kwargs)

    def wtr(self) -> WorkingTimeRange | None:
        """returns WorkingTimeRange that matches this TimeEntry."""

        # get a list ot WorkingTimeRanges for this day
        working_hours = self.work_schedule.working_hours.filter(
            weekday=self.start.weekday()
        )
        # if no working_hours are defined yet, just return empty WTR
        if not working_hours:
            return None

        thetime = self.start
        match = (
            working_hours.filter(start_time__lte=thetime, end_time__gt=thetime)
            .order_by("-start_time")
            .first()
        )
        if not match:
            next_wtr = (
                working_hours.filter(start_time__gt=thetime)
                .order_by("start_time")
                .first()
            )
            prev_wtr = (
                working_hours.filter(end_time__lte=thetime)
                .order_by("-end_time")
                .first()
            )
            if next_wtr and prev_wtr:
                if (thetime - prev_wtr.end).total_seconds() < (
                    next_wtr.start - thetime
                ).total_seconds():
                    match = prev_wtr
                else:
                    match = next_wtr
            elif next_wtr:
                # there is only a next block, no previous
                match = next_wtr
            else:
                # there is only a previous block, and no next one.
                match = prev_wtr
        return match

    def delta(self, recalculate=False) -> timedelta:
        """returns calculated delta between current duration and scheduled duration.

        Note:
            the WTR (incl. cached_delta) is not saved in this method. This must be done manually.
        """
        if recalculate or not self.cached_delta:
            wtr = self.wtr()
            if not wtr:
                return timedelta()
            self.cached_delta = self.duration() - wtr.duration()
        return self.cached_delta

    def delta_h(self) -> float:
        delta = self.delta()
        if delta.days < 0:
            sign = -1
        else:
            sign = 1

        total_seconds = abs(delta.seconds)
        return total_seconds / 60 / 60 * sign
        # hours = total_seconds // 3600
        # minutes = (total_seconds % 3600) // 60
        # return f"{sign}{hours}:{minutes}"


class HolidayType(models.Model):
    """Type of holiday: normal, special,..."""

    name = models.CharField(max_length=255)
    # color = ColorField(blank=True, null=True)

    def __str__(self):
        return self.name


class HolidayStatus(TextChoices):
    NEW = ("new", _("New"))
    APPROVED = ("approved", _("Approved"))
    # CONSUMED = APPROVED and date < today
    DECLINED = ("declined", _("Declined"))


class Holiday(models.Model):
    """Represents one holiday for one user."""

    class Meta:
        unique_together = ["day", "employee"]
        permissions = (
            (
                "administer_holiday",
                _("Can administer holidays"),
            ),
        )

    day = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.ForeignKey(HolidayType, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=25, choices=HolidayStatus.choices, default=HolidayStatus.NEW
    )

    def __str__(self):
        # confirmed = "✅" if self.status == HolidayStatus.CONFIRMED else "❌"
        return f"{self.employee}: {date_format(self.day,'SHORT_DATE_FORMAT')} ({self.type}) [{self.status}]"

from datetime import timedelta

from django.contrib.auth.signals import user_logged_in
from django.db.models import QuerySet
from django.utils.timezone import now

# from medux import notifications
from medux.plugins.timetracker.models import TimeEntry


def notify_employee_after_login_for_open_timeentries(**kwargs):
    user = kwargs["user"]
    if hasattr(user, "employee"):
        employee = user.employee
        if employee.active_work_schedule:
            # search for started, but unfinished timeentries of the current user
            current_timeentries: QuerySet = TimeEntry.objects.filter(
                work_schedule=employee.active_work_schedule,
                end=None,
                start__lt=now() + timedelta(minutes=15),
                # work_schedule__working_hours__week_day=today().weekday(),
            )
            # there are unfinished timeentries, notify user
            # notifications.success(
            #     kwargs["user"],
            #     "There are unfinished time entries.",  # TODO link to Timetracker
            #     dismissible=True,
            # )


user_logged_in.connect(notify_employee_after_login_for_open_timeentries)

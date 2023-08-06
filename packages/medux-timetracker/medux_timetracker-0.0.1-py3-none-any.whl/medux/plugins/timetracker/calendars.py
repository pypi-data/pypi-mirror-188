import datetime
from calendar import (
    LocaleHTMLCalendar,
    month_name,
    January,
    different_locale,
)
import holidays
from dateutil.utils import today
from django.db.models import QuerySet
from django.template import Engine, Context

from medux.common.tools import django_locale_to_country_code
from medux.employees.models import Employee
from medux.plugins.timetracker.models import Holiday, HolidayStatus


def get_holiday_context_from_day(
    employee: Employee,
    thedate: datetime.date,
    queryset: QuerySet[Holiday],
    locale: tuple,
) -> dict:
    """Helper function that creates context for one holiday.

    Returns:
        context: a dict with usable context for rendering one day:
            day: the date of the day to render
            object: the Holiday object of the employee
            type: the `HolidayType` of the holiday
            status: the `HolidayStatus` of the holiday
    """

    context = {}
    context["day"] = thedate
    try:
        obj = queryset.get(employee_id=employee.id, day=thedate)
        context["object"] = obj
        context["status"] = obj.status
        context["type"] = obj.type
        context["approved"] = obj.status == HolidayStatus.APPROVED
        context["declined"] = obj.status == HolidayStatus.DECLINED
        context["consumed"] = (
            obj.status == HolidayStatus.APPROVED and thedate < today().date()
        )
    except Holiday.DoesNotExist:
        obj = False
    context["collisions"] = queryset.filter(day=thedate).order_by("employee_id")
    country_code = django_locale_to_country_code(locale)
    is_public = thedate in holidays.country_holidays(country_code)
    context["public"] = is_public

    is_weekend = thedate.weekday() in [5, 6]
    context["weekend"] = is_weekend

    is_editable = (
        not is_weekend
        and not is_public
        and (not obj or obj.status == HolidayStatus.NEW)
    )
    context["editable"] = is_editable
    return context


class HolidayCalendar(LocaleHTMLCalendar):
    queryset = None

    def __init__(self, employee: Employee, queryset=None, locale=None, firstweekday=0):
        self.queryset = queryset or Holiday.objects.none()
        self.employee = employee
        super().__init__(firstweekday, locale)

    def formatday(self, thedate: datetime.date):
        """Return a day as a table cell."""
        context = get_holiday_context_from_day(
            employee=self.employee,
            thedate=thedate,
            queryset=self.queryset,
            locale=self.locale,
        )
        return (
            Engine.get_default()
            .get_template("timetracker/day.html")
            .render(Context(context))
        )

    def formatmonthname(self, theyear, themonth):
        """Return a month name as a table header."""
        with different_locale(self.locale):
            return f"<th class='{self.cssclass_month_head}'>{month_name[themonth]}</th>"

    def formatmonth(self, theyear, themonth):
        """
        Return a month as a table row.
        """
        v = []
        a = v.append
        a('<tr class="month">')
        a(self.formatmonthname(theyear, themonth))
        for week in self.monthdatescalendar(theyear, themonth):
            for day in week:
                if day.month == themonth:
                    a(self.formatday(day))

        a("</tr>")
        return "".join(v)

    def formatyear(self, employee, theyear):
        """
        Return a formatted year as a table with months as rows.
        """
        self.queryset = self.queryset.filter(day__year=theyear)
        v = []
        a = v.append
        a('<div class="table-responsive">')
        a(f"<table class='table table-borderless {self.cssclass_year}'>")
        for month in range(January, January + 12):
            a(self.formatmonth(theyear, month))
        a("</table>")
        a("</div>")
        return "".join(v)

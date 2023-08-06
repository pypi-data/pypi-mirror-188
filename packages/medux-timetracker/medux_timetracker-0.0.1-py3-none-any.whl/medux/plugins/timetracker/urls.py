from django.contrib.auth import get_user_model
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from medux.plugins.timetracker.models import TimeEntry
from . import views

User = get_user_model()

app_name = "timetracker"


class TimeEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeEntry
        fields = "__all__"


class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r"users", UserViewSet)
# router.register(r"timeentries", TimeEntryViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("overview/", views.OverView.as_view(), name="overview"),
    path(
        "overview/<int:year>/<int:month>/",
        views.OverView.as_view(),
        name="overview-month",
    ),
    path("holidays/", views.HolidaysView.as_view(), name="current-holidays"),
    path("holidays/<int:year>/", views.HolidaysView.as_view(), name="holidays"),
    path(
        "toggle-holiday/<int:year>/<int:month>/<int:day>/",
        views.ToggleHolidayView.as_view(),
        name="toggle-holiday",
    ),
    path(
        "set-holiday-status/<pk>/<str:status>",
        views.HolidaySetStatusView.as_view(),
        name="set-holiday-status",
    ),
    path("admin/", views.AdminView.as_view(), name="admin"),
    path(
        "pending-holidays/",
        views.PendingHolidayRequestsView.as_view(),
        name="pending-holiday-requests",
    ),
    path(
        "delete-holiday/<pk>/", views.DeleteHolidayView.as_view(), name="delete-holiday"
    ),
    # TimeEntries
    path("timeentry/", views.TimeEntryListView.as_view(), name="timeentry-list"),
    path("timeentry/add/", views.TimeEntryCreateView.as_view(), name="timeentry-add"),
    path(
        "timeentry/<pk>/change/",
        views.TimeEntryUpdateView.as_view(),
        name="timeentry-update",
    ),
    path(
        "timeentry/<pk>/delete/",
        views.TimeEntryDeleteView.as_view(),
        name="timeentry-delete",
    ),
    # WorkingTimeRange
    path(
        "work_schedule/",
        views.CurrentWorkScheduleView.as_view(),
        name="current-work-schedule",
    ),
    # generic
    path("logout/", views.LogoutWithTimeTrackingView.as_view(), name="logout"),
]

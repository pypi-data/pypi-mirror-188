from django.urls import path

from .views import IndexView, SendView, SettingsView

urlpatterns = [
    path(
        "control/event/<str:organizer>/<str:event>/settings/simple_test_results/",
        SettingsView.as_view(),
        name="settings",
    ),
    path(
        "control/event/<str:organizer>/<str:event>/simple_test_results/",
        IndexView.as_view(),
        name="index",
    ),
    path(
        "control/event/<str:organizer>/<str:event>/simple_test_results/<str:pk>/send/",
        SendView.as_view(),
        name="send",
    ),
]

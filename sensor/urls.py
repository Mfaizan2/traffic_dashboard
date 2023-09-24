from django.urls import path

from sensor.views import (
    SensorDataView,
    SensorDataDashboardView,
    SensorSpeedDataView,
)

urlpatterns = [
    path("sensors_data/", SensorDataView.as_view(), name="sensors_data"),
    path("sensor_speed_data/", SensorSpeedDataView.as_view(), name="sensor_speed_data"),
    path("", SensorDataDashboardView.as_view(), name="dashboard"),
]

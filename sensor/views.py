from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sensor.models import SensorData, Vehicle
from sensor.serializer import SensorDataSerializer, SensorSpeedDataSerializer


class SensorDataView(APIView):
    def get(self, request):
        """
        That view will return max 100 sensors data against min_latitude, max_latitude,
        min_longitude, max_longitude and date query params.
        In-case, no query param is provided, it will return the latest 100 sensors data.
        """
        response = {
            "status": status.HTTP_200_OK,
            "message": "Request processed successfully",
            "data": [],
        }

        min_latitude = request.query_params.get("min_latitude", None)
        max_latitude = request.query_params.get("max_latitude", None)
        min_longitude = request.query_params.get("min_longitude", None)
        max_longitude = request.query_params.get("max_longitude", None)
        date_str = request.query_params.get("date", None)

        try:
            filter_conditions = Q()

            if (
                min_latitude is not None
                and min_latitude != ""
                and max_latitude is not None
                and max_latitude != ""
            ):
                filter_conditions &= Q(
                    latitude__range=(max_latitude, min_latitude)
                ) | Q(latitude__range=(min_latitude, max_latitude))

            if (
                min_longitude is not None
                and min_longitude != ""
                and max_longitude is not None
                and max_longitude != ""
            ):
                filter_conditions &= Q(
                    longitude__range=(min_longitude, max_longitude)
                ) | Q(longitude__range=(max_longitude, min_longitude))

            if date_str is not None and date_str != "":
                date_str = date_str.split("/")
                start_date = datetime.strptime(date_str[0], "%Y-%m-%d")
                end_date = datetime.strptime(date_str[1], "%Y-%m-%d")
                filter_conditions &= Q(timestamp__date__range=(start_date, end_date))

            sensor_data = (
                SensorData.objects.filter(filter_conditions)
                .order_by("vehicle__name", "-timestamp")
                .distinct("vehicle__name")[:100]
            )

            serializer = SensorDataSerializer(sensor_data, many=True)
            response["data"] = serializer.data
            return Response(response, status=response["status"])

        except Exception as e:
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = e.__str__()

        return Response(response, status=response["status"])


class SensorSpeedDataView(APIView):
    def get(self, request):
        """
        That view will return max last 10 sensor speed data entries.
        In-case, no query param is provided, it will return 400 bad request error.
        """
        response = {
            "status": status.HTTP_200_OK,
            "message": "Request processed successfully",
            "data": [],
        }

        name = request.query_params.get("name", None)

        if not name:
            response["status"] = status.HTTP_400_BAD_REQUEST
            response["message"] = "Name param is missing in request!!!"
            return Response(response, status=response["status"])

        try:
            vehicle_obj = Vehicle.objects.get(name=name)
        except ObjectDoesNotExist:
            response["status"] = status.HTTP_404_NOT_FOUND
            response["message"] = "Vehicle with that name not found!!!"
            return Response(response, status=response["status"])

        try:
            filter_conditions = Q()

            if name is not None and name != "":
                filter_conditions &= Q(vehicle__name=name)

            sensor_data = list(
                SensorData.objects.filter(filter_conditions).values(
                    "timestamp", "vehicle_speed", "speed_limit"
                )[:10]
            )

            serializer = SensorSpeedDataSerializer(sensor_data, many=True)
            response["data"] = serializer.data
            return Response(response, status=response["status"])

        except Exception as e:
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = e.__str__()

        return Response(response, status=response["status"])


class SensorDataDashboardView(View):
    def get(self, request):
        return render(request, "dashboard.html")

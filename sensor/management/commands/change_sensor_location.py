from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from sensor.models import SensorData, Vehicle
from datetime import datetime


class Command(BaseCommand):
    help = "Change sensor location"

    def add_arguments(self, parser):  # adding the vehicle_name param
        parser.add_argument("--vehicle_name", type=str, default=None, required=True)

    def handle(self, *args, **options):
        """
        This handle function will change the vehicle position.
        First it will check that vehicle_name is provided as param or not. If yes, then it will update
        the vehicle location
        """
        vehicle_name = options["vehicle_name"]
        if not vehicle_name:
            self.stdout.write(
                self.style.ERROR("Error: --vehicle_name is not provided.")
            )
            return

        try:
            vehicle_obj = Vehicle.objects.get(name=vehicle_name)
        except ObjectDoesNotExist:
            self.stdout.write(
                self.style.ERROR("Error: No Vehicle found with that name.")
            )
            return

        try:
            # Getting the latest vehicle location
            recent_sensor_obj = SensorData.objects.filter(vehicle=vehicle_obj).order_by(
                "-id"
            )[0]

            # Creating a new record for sensor location
            sensor_new_entry = SensorData(vehicle=vehicle_obj)
            sensor_new_entry.latitude = recent_sensor_obj.latitude + 0.001
            sensor_new_entry.longitude = recent_sensor_obj.longitude + 0.001
            sensor_new_entry.vehicle_speed = recent_sensor_obj.vehicle_speed + 14
            sensor_new_entry.speed_limit = recent_sensor_obj.speed_limit + 14
            sensor_new_entry.timestamp = datetime.now()

            sensor_new_entry.save()

            self.stdout.write(
                self.style.SUCCESS("Vehicle location changed successfully")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(e.__str__()))

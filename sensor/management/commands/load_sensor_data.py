from django.core.management.base import BaseCommand

from sensor.models import SensorData, Vehicle
from random import uniform
from datetime import datetime, timedelta

# Some cities coordinate to dump the data accordingly
# max_latitude, min_latitude, max_longitude, min_longitude
city_coordinates = {
    "New York": (
        40.7128,
        40.4774,
        -73.9097,
        -74.2591,
    ),
    "Los Angeles": (34.0522, 33.7037, -118.1609, -118.6682),
    "Chicago": (41.8781, 41.6446, -87.5240, -87.9401),
    "San Francisco": (37.7749, 37.6398, -122.3483, -123.1738),
    "Lahore": (31.5497, 31.4715, 74.3784, 74.2179),
    "Sydney": (-33.5675, -34.1072, 151.3430, 150.5209),
}


class Command(BaseCommand):
    help = "Load 5000 sensor data records into the database"

    def add_arguments(self, parser):
        parser.add_argument("--city", type=str, default=None, required=True)

    def handle(self, *args, **options):
        """
        This handle function will load the vehicles and sensors data as per city pass in param.
        First it will check that city is provided as param or not. If yes, then it will create 500 vehicles
        and sensors data in db.
        """
        city = options["city"]
        if not city:
            self.stdout.write(self.style.ERROR("Error: --city is not provided."))
            return
        if city not in city_coordinates:
            self.stdout.write(
                self.style.ERROR(
                    "Error: Please pass the arguments in [New York, Los Angeles, Chicago, "
                    "San Francisco]"
                )
            )
            return

        self.stdout.write(self.style.SUCCESS("Loading sensor data..."))

        coordinates = city_coordinates[city]
        max_latitude, min_latitude, max_longitude, min_longitude = coordinates

        vehicle_data_to_insert = []
        data_to_insert = []

        try:
            for counter in range(500):
                latitude = round(uniform(max_latitude, min_latitude), 6)
                longitude = round(uniform(max_longitude, min_longitude), 6)
                timestamp = datetime.now() - timedelta(days=uniform(1, 7))
                vehicle_speed = round(uniform(0, 120), 2)
                speed_limit = round(uniform(0, 120), 2)

                vehicle_obj = Vehicle.objects.create(name=f"{city}_vehicle_{counter}")

                data_to_insert.append(
                    SensorData(
                        vehicle=vehicle_obj,
                        latitude=latitude,
                        longitude=longitude,
                        timestamp=timestamp,
                        vehicle_speed=vehicle_speed,
                        speed_limit=speed_limit,
                    )
                )

            Vehicle.objects.bulk_create(vehicle_data_to_insert)
            SensorData.objects.bulk_create(data_to_insert)

            self.stdout.write(self.style.SUCCESS("Loaded 500 sensor data records."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(e.__str__()))

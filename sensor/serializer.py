from rest_framework import serializers
from sensor.models import SensorData


class SensorDataSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="vehicle.name", read_only=True)

    class Meta:
        model = SensorData
        fields = ("name", "latitude", "longitude", "timestamp")


class SensorSpeedDataSerializer(serializers.ModelSerializer):
    deviation = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = SensorData
        fields = ("timestamp", "vehicle_speed", "speed_limit", "deviation")

    def get_deviation(self, obj):
        # Calculate and return the deviation here
        return obj["vehicle_speed"] - obj["speed_limit"]

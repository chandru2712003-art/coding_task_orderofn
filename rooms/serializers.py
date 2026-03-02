from rest_framework import serializers
from .models import MeetingRoom, Booking


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ["id", "name", "capacity"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room", "start_time", "end_time"]
        read_only_fields = ["id", "room"]

    def validate(self, data):
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError("End time must be after start time.")
        return data
    
class MeetingRoomCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ["id", "name", "capacity", "is_active"]

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be greater than 0.")
        return value    
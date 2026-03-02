from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import MeetingRoom, Booking, History
from .serializers import (
    MeetingRoomSerializer, 
    BookingSerializer, 
    MeetingRoomCreateUpdateSerializer
)


class BookMeetingRoomView(APIView):

    @transaction.atomic
    def post(self, request, room_id):
        room = get_object_or_404(MeetingRoom, pk=room_id, is_active=True)

        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = Booking(
            room=room,
            start_time=serializer.validated_data["start_time"],
            end_time=serializer.validated_data["end_time"],
        )

        booking.save()

        History.objects.create(
            booking=booking,
            action="BOOKED"
        )

        return Response(
            {"message": "Booking successful"},
            status=status.HTTP_201_CREATED
        )


class AvailableMeetingRoomsView(ListAPIView):


    serializer_class = MeetingRoomSerializer

    def get_queryset(self):
        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")

        queryset = MeetingRoom.objects.filter(is_active=True)

        if start_time and end_time:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)

            if start_time and end_time:
                queryset = queryset.exclude(
                    bookings__start_time__lt=end_time,
                    bookings__end_time__gt=start_time
                )

        return queryset.distinct()
    
class CreateMeetingRoomView(generics.CreateAPIView):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomCreateUpdateSerializer    

class UpdateRoomAvailabilityView(APIView):

    def patch(self, request, room_id):
        room = get_object_or_404(MeetingRoom, pk=room_id)

        is_active = request.data.get("is_active")

        if is_active is None:
            return Response(
                {"error": "is_active field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        room.is_active = bool(is_active)
        room.save()

        return Response(
            {
                "message": "Room availability updated successfully.",
                "room_id": room.id,
                "is_active": room.is_active
            },
            status=status.HTTP_200_OK
        )    
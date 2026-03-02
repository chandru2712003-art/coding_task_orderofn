from django.urls import path
from . import views

urlpatterns = [
    path(
        "meeting-rooms/<int:room_id>/book/",
        views.BookMeetingRoomView.as_view(),
        name="book-room"
    ),
    path(
        "meeting-rooms/available/",
        views.AvailableMeetingRoomsView.as_view(),
        name="available-rooms"
    ),

    path(
        "meeting-rooms/",
        views.CreateMeetingRoomView.as_view(),
        name="create-room"
    ),
    path(
        "meeting-rooms/<int:room_id>/availability/",
        views.UpdateRoomAvailabilityView.as_view(),
        name="update-room-availability"
    ),
]
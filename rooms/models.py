from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class MeetingRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.capacity})"


class Booking(models.Model):
    room = models.ForeignKey(
        MeetingRoom,
        related_name="bookings",
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_time"]
        indexes = [
            models.Index(fields=["start_time", "end_time"]),
        ]

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be greater than start time.")

        if self.start_time < timezone.now():
            raise ValidationError("Cannot book for past time.")

        overlapping = Booking.objects.filter(
            room=self.room,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("Room is not available for the selected time range.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class History(models.Model):
    booking = models.ForeignKey(
        Booking,
        related_name="history",
        on_delete=models.CASCADE
    )
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
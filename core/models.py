from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    # NEW (temporarily nullable)
    aadhar_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    aadhar_last4 = models.CharField(max_length=4, null=True, blank=True)

    phone = models.CharField(max_length=15)

    # Legacy plaintext (keep for now so we can backfill; make nullable)
    aadhar = models.CharField(max_length=12, unique=True, null=True, blank=True)


class Booking(models.Model):
    STATUS_CHOICES = [("CONFIRMED","Confirmed"), ("CANCELLED","Cancelled"), ("WAITLIST","Waitlisted")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    pnr  = models.CharField(max_length=10, unique=True, editable=False)
    route = models.CharField(max_length=200)           # e.g., "Chennai → Bangalore"
    travel_date = models.DateField()
    cls = models.CharField(max_length=32)              # e.g., "SL", "3A"
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="CONFIRMED")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = "".join([get_random_string(1, allowed_chars="0123456789") for _ in range(10)])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pnr} - {self.route} {self.travel_date}"


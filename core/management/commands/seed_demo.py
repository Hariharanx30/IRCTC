from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Booking
from datetime import date

class Command(BaseCommand):
    help = "Seed demo user and a couple of bookings"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(username="123456789012", defaults={"first_name":"Hari"})
        Profile.objects.get_or_create(user=user, defaults={"aadhar":"123456789012","phone":"9876543210"})
        Booking.objects.get_or_create(user=user, route="Chennai → Bangalore", travel_date=date(2025,8,5), cls="SL", amount=450)
        Booking.objects.get_or_create(user=user, route="Mumbai → Delhi", travel_date=date(2025,8,12), cls="3A", amount=1850)
        self.stdout.write(self.style.SUCCESS("Seeded demo data"))

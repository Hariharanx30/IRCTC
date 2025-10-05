from django.contrib import admin
from .models import Profile, Booking

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user","aadhar","phone")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("pnr","user","route","travel_date","cls","status","amount","created_at")
    list_filter = ("status","cls","travel_date")
    search_fields = ("pnr","route","user__username","user__first_name")

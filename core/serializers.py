from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Booking
from .utils import validate_aadhar, validate_phone, normalize_aadhar, normalize_phone

class RegisterSerializer(serializers.Serializer):
    aadhar = serializers.CharField(max_length=12)
    phone  = serializers.CharField(max_length=15)
    name   = serializers.CharField(max_length=120)

    def validate(self, attrs):
        if not validate_aadhar(attrs["aadhar"]):
            raise serializers.ValidationError("Invalid Aadhaar (12 digits).")
        if not validate_phone(attrs["phone"]):
            raise serializers.ValidationError("Invalid phone (10 digits).")
        return attrs

class ExistingLoginSerializer(serializers.Serializer):
    aadhar = serializers.CharField(max_length=12)
    phone  = serializers.CharField(max_length=15)

    def validate(self, attrs):
        if not validate_aadhar(attrs["aadhar"]):
            raise serializers.ValidationError("Invalid Aadhaar (12 digits).")
        if not validate_phone(attrs["phone"]):
            raise serializers.ValidationError("Invalid phone (10 digits).")
        return attrs

class UserSerializer(serializers.ModelSerializer):
    masked_aadhar = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "masked_aadhar", "phone"]
    def get_masked_aadhar(self, obj):
        p = getattr(obj, "profile", None)
        return f"XXXX-XXXX-{p.aadhar_last4}" if p else None
    def get_phone(self, obj):
        return getattr(obj.profile, "phone", None)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["pnr", "route", "travel_date", "cls", "status", "amount", "created_at"]

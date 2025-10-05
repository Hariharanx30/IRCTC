from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile, Booking
from .serializers import (
    # NEW serializers you created in serializers.py
    RegisterSerializer,        # {aadhar, name, phone}
    ExistingLoginSerializer,   # {aadhar, phone}
    UserSerializer,
    BookingSerializer,
)
from .utils import (
    hash_aadhar,
    normalize_aadhar,
    normalize_phone,
)

def _issue_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}

# ------------------ NEW: Register (new users) ------------------
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    New user registration
    Body: { "aadhar":"12-digit", "name":"Full Name", "phone":"10-digit" }
    If Aadhaar exists -> 409 (tell them to use login)
    Else create user+profile (Aadhaar hashed) and issue tokens.
    """
    ser = RegisterSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    aadhar = normalize_aadhar(ser.validated_data["aadhar"])
    phone  = normalize_phone(ser.validated_data["phone"])
    name   = ser.validated_data["name"].strip()

    ahash = hash_aadhar(aadhar)

    # If someone already registered with this Aadhaar, block duplicate
    if Profile.objects.filter(aadhar_hash=ahash).exists():
        return Response({"detail": "User already exists. Please log in."}, status=409)

    # Create a unique username (don’t store Aadhaar in username anymore)
    base_username = f"user_{phone}" if phone else "user"
    username = base_username
    i = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{i}"
        i += 1

    user = User.objects.create(username=username, first_name=name)
    Profile.objects.create(
        user=user,
        aadhar_hash=ahash,
        aadhar_last4=aadhar[-4:],
        phone=phone,
        # If you still have legacy plaintext column, keep it None on new records
        aadhar=None,
    )

    tokens = _issue_tokens_for_user(user)
    return Response({"user": UserSerializer(user).data, **tokens}, status=201)

# --------------- NEW: Login (existing users) -------------------
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_existing(request):
    """
    Existing user login
    Body: { "aadhar":"12-digit", "phone":"10-digit" }
    Finds Profile by (aadhar_hash + phone) and issues tokens.
    """
    ser = ExistingLoginSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    aadhar = normalize_aadhar(ser.validated_data["aadhar"])
    phone  = normalize_phone(ser.validated_data["phone"])
    ahash = hash_aadhar(aadhar)

    try:
        prof = Profile.objects.get(aadhar_hash=ahash, phone=phone)
    except Profile.DoesNotExist:
        return Response({"detail": "No account found. Please register first."}, status=404)

    tokens = _issue_tokens_for_user(prof.user)
    return Response({"user": UserSerializer(prof.user).data, **tokens})

# (Optional) Keep old login route temporarily but point it to login_existing
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    """Deprecated: use /api/login/ as existing login; this delegates."""
    return login_existing(request)

# --------------------- Existing endpoints ----------------------

@api_view(["GET"])
def me(request):
    return Response(UserSerializer(request.user).data)

@api_view(["GET"])
def my_bookings(request):
    qs = Booking.objects.filter(user=request.user).order_by("-created_at")
    return Response(BookingSerializer(qs, many=True).data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def pnr_status(request, pnr):
    booking = get_object_or_404(Booking, pnr=pnr)
    return Response({
        "pnr": booking.pnr, "route": booking.route,
        "travel_date": booking.travel_date, "class": booking.cls,
        "status": booking.status, "amount": str(booking.amount),
    })

@api_view(["POST"])
def cancel_booking(request):
    pnr = request.data.get("pnr")
    if not pnr:
        return Response({"detail": "PNR is required."}, status=400)
    booking = get_object_or_404(Booking, pnr=pnr, user=request.user)
    if booking.status == "CANCELLED":
        return Response({"detail": "Already cancelled."}, status=400)
    booking.status = "CANCELLED"
    booking.save()
    return Response({"detail": "Cancellation successful.", "pnr": booking.pnr})

from decimal import Decimal

@api_view(["POST"])
def create_booking(request):
    """
    Create a booking for the logged-in user.
    Body: { "route": "Chennai → Bangalore", "travel_date": "YYYY-MM-DD", "cls": "SL|3A|2A|1A|CC|EC", "amount": 450 }
    """
    data = request.data
    missing = [k for k in ("route", "travel_date", "cls", "amount") if k not in data or str(data[k]).strip() == ""]
    if missing:
        return Response({"detail": f"Missing fields: {', '.join(missing)}"}, status=400)

    route = str(data["route"]).strip()
    cls = str(data["cls"]).strip().upper()
    if cls not in {"SL", "3A", "2A", "1A", "CC", "EC"}:
        return Response({"detail": "Invalid class. Use one of SL, 3A, 2A, 1A, CC, EC."}, status=400)

    try:
        travel_date = str(data["travel_date"]).strip()
        amt = Decimal(str(data["amount"]))
        if amt < 0:
            return Response({"detail": "Amount must be ≥ 0."}, status=400)
    except Exception:
        return Response({"detail": "Invalid travel_date or amount format."}, status=400)

    booking = Booking.objects.create(
        user=request.user,
        route=route,
        travel_date=travel_date,
        cls=cls,
        amount=amt,
        status="CONFIRMED"
    )
    return Response(BookingSerializer(booking).data, status=201)

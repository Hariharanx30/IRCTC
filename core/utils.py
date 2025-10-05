import hashlib
import re
from django.conf import settings

# Aadhaar = 12 digits, Phone = 10 digits (basic checks)
AADHAAR_RE = re.compile(r"^\d{12}$")
PHONE_RE   = re.compile(r"^\d{10}$")

def normalize_aadhar(aadhar: str) -> str:
    """Strip non-digits, return Aadhaar as 12 digits if possible"""
    return re.sub(r"\D", "", aadhar or "")

def normalize_phone(phone: str) -> str:
    """Strip non-digits, return phone as only digits"""
    return re.sub(r"\D", "", phone or "")

def hash_aadhar(aadhar: str) -> str:
    """
    Hash Aadhaar securely (SHA-256 with a pepper).
    Add a secret pepper in settings.py like:
        AADHAAR_PEPPER = "some-random-secret-string"
    """
    norm = normalize_aadhar(aadhar)
    pepper = getattr(settings, "AADHAAR_PEPPER", "dev-pepper-change-me")
    return hashlib.sha256((pepper + norm).encode("utf-8")).hexdigest()

def validate_aadhar(aadhar: str) -> bool:
    """Check if Aadhaar looks like 12 digits"""
    return bool(AADHAAR_RE.match(normalize_aadhar(aadhar)))

def validate_phone(phone: str) -> bool:
    """Check if phone looks like 10 digits"""
    return bool(PHONE_RE.match(normalize_phone(phone)))

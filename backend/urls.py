"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from core import views as api

urlpatterns = [
    # UI pages
    path("", TemplateView.as_view(template_name="login.html")),            # /
    path("login/", TemplateView.as_view(template_name="login.html")),
     path("register/", TemplateView.as_view(template_name="register.html")),
    path("home/", TemplateView.as_view(template_name="home.html")),
    path("history/", TemplateView.as_view(template_name="history.html")),
    path("pnr/", TemplateView.as_view(template_name="pnr.html")),
    path("cancel/", TemplateView.as_view(template_name="cancel.html")),
    path("tourism/", TemplateView.as_view(template_name="tourism.html")),
    path("booking/", TemplateView.as_view(template_name="booking.html")),

    # API
    path("admin/", admin.site.urls),
    path("api/register/", api.register),        # NEW (for new users)
    path("api/login/",    api.login_existing),  # existing users
    path("api/me/", api.me),
    path("api/bookings/", api.my_bookings),
    path("api/pnr/<str:pnr>/", api.pnr_status),
    path("api/cancel/", api.cancel_booking),
    path("api/book/", api.create_booking),
]


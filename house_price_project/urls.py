from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", account_views.landing, name="landing"),

    path("accounts/", include("accounts.urls")),

    path("", include("predictor.urls")),
]
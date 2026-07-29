from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm


# -----------------------------
# Landing Page
# -----------------------------
def landing(request):
    return render(request, "landing.html")


# -----------------------------
# Signup
# -----------------------------
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard_redirect")

    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


# -----------------------------
# Login
# -----------------------------
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,
                            username=username,
                            password=password)

        if user is not None:

            login(request, user)

            if user.is_staff:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


# -----------------------------
# Logout
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect("landing")


# -----------------------------
# Profile
# -----------------------------
def profile(request):
    return render(request, "accounts/profile.html")
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from adoption.services import pet_service


def home(request: HttpRequest) -> HttpResponse:
    """Send unauthenticated users to the login page."""
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def register(request: HttpRequest) -> HttpResponse:
    """Redirect standalone register requests to the login page."""
    return redirect("login")


def login_view(request: HttpRequest) -> HttpResponse:
    """Render the login form and authenticate the user."""
    if request.user.is_authenticated:
        return redirect("dashboard")

    is_register_post = request.method == "POST" and request.POST.get("form_type") == "register"

    login_form = AuthenticationForm(
        request,
        data=request.POST if request.method == "POST" and not is_register_post else None,
    )
    register_form = UserCreationForm(
        request.POST if is_register_post else None,
    )

    if request.method == "POST":
        if is_register_post:
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect("dashboard")
        else:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("dashboard")

            # Allow login by email if username login fails
            username_or_email = request.POST.get("username")
            password = request.POST.get("password")
            if username_or_email and password:
                UserModel = get_user_model()
                user_by_email = UserModel.objects.filter(email__iexact=username_or_email).first()
                if user_by_email:
                    user = authenticate(request, username=user_by_email.username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect("dashboard")

    return render(
        request,
        "adoption/login.html",
        {"form": login_form, "register_form": register_form},
    )


@login_required
def dashboard_home(request: HttpRequest) -> HttpResponse:
    """Show the main dashboard home page with stats after login."""
    available_pet_count = pet_service.get_available_pet_count()
    adoption_request_count = pet_service.get_adoption_request_count()

    context = {
        "page_title": "Dashboard",
        "available_pet_count": available_pet_count,
        "adoption_request_count": adoption_request_count,
    }
    return render(request, "adoption/dashboard_home.html", context)


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("login")


@login_required
def about_us(request: HttpRequest) -> HttpResponse:
    """Show the About Us page."""
    return render(request, "adoption/about_us.html")


@login_required
def settings(request: HttpRequest) -> HttpResponse:
    """Show the Settings page."""
    user_email = request.user.email
    context = {
        "user_email": user_email,
    }
    return render(request, "adoption/settings.html", context)

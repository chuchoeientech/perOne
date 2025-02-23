from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")  # Si no está autenticado, lo manda al login
    # Si está autenticado, lo redirige a la página principal
    return redirect("index")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Cambia "home" por la vista a la que quieres redirigir tras login
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirige al login tras cerrar sesión


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El email ya está en uso")
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password1)
            user.save()
            messages.success(
                request, "Registro exitoso. Ahora puedes iniciar sesión")
            return redirect("login")

    return render(request, "authentication/register.html")

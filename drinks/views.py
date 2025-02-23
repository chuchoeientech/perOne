from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import DrinkSession
import uuid


def home(request):
    session_id = request.session.get("session_id")

    # Si no tiene sesión, crear una nueva
    if not session_id:
        session_id = str(uuid.uuid4())  # Genera un ID único
        request.session["session_id"] = session_id
        DrinkSession.objects.create(session_id=session_id)

    session = DrinkSession.objects.get(session_id=session_id)

    return render(request, "drinks/index.html", {
        "beer_count": session.beer_count,
        "session_id": session_id
    })


def update_beer_count(request):
    if request.method == "POST":
        session_id = request.session.get("session_id")
        if not session_id:
            return JsonResponse({"error": "Session not found"}, status=400)

        session = get_object_or_404(DrinkSession, session_id=session_id)
        session.beer_count += 1
        session.save()
        return JsonResponse({"beer_count": session.beer_count})

    return JsonResponse({"error": "Invalid request"}, status=400)


def finish_session(request):
    if request.method == "POST":
        session_id = request.session.get(
            "session_id")  # Tomar la sesión activa
        beer_price = float(request.POST.get("beer_price", 0))

        session = get_object_or_404(DrinkSession, session_id=session_id)
        total = session.total_price(beer_price)
        total_with_tip = session.total_price_with_tip(beer_price)

        # Eliminar la sesión actual
        del request.session["session_id"]

        # Crear una nueva sesión vacía
        new_session_id = str(uuid.uuid4())
        request.session["session_id"] = new_session_id
        new_session = DrinkSession.objects.create(session_id=new_session_id)

        return JsonResponse({
            "beer_count": session.beer_count,
            "total_price": total,
            "total_price_with_tip": total_with_tip,
            "new_session_id": new_session_id  # Enviar el nuevo session_id
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import DrinkSession
import uuid


def home(request):
    session_id = request.session.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())  # Genera un ID único
        request.session["session_id"] = session_id
        DrinkSession.objects.create(session_id=session_id)

    session = DrinkSession.objects.get(session_id=session_id)

    past_sessions = DrinkSession.objects.exclude(
        session_id=session_id).order_by("-timestamp")[:10]

    beer_price = int(request.GET.get("beer_price", 10000)
                     )  # Valor predeterminado: 10000

    sessions_data = []
    for s in past_sessions:
        sessions_data.append({
            "beer_count": s.beer_count,
            "total_price": s.total_price(beer_price),  # Valor numérico
            # Valor numérico
            "total_with_tip": s.total_price_with_tip(beer_price),
            "timestamp": s.timestamp.strftime("%d/%m/%Y %H:%M")
        })

    return render(request, "drinks/index.html", {
        "beer_count": session.beer_count,
        "session_id": session_id,
        "sessions": sessions_data,
        "beer_price": beer_price  # Pasar el valor al template
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
        session_id = request.session.get("session_id")
        beer_price = int(request.POST.get("beer_price", 0)
                         )  # Asegurar tipo entero

        session = get_object_or_404(DrinkSession, session_id=session_id)
        total = session.total_price(beer_price)
        total_with_tip = session.total_price_with_tip(beer_price)

        # 🔍 Agregar print para depurar
        print(
            f"🔍 DEBUG: Precio unitario: {beer_price}, Cantidad: {session.beer_count}, Total: {total}, Con propina: {total_with_tip}")

        # Eliminar la sesión actual
        del request.session["session_id"]

        # Crear una nueva sesión vacía
        new_session_id = str(uuid.uuid4())
        request.session["session_id"] = new_session_id
        new_session = DrinkSession.objects.create(session_id=new_session_id)

        return JsonResponse({
            "beer_count": session.beer_count,
            "total_price": f"{total:,} Gs.",  # Formatear correctamente
            "total_price_with_tip": f"{total_with_tip:,} Gs.",
            "new_session_id": new_session_id
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

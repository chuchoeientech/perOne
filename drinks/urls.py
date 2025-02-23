from django.urls import path
from .views import home, update_beer_count, finish_session

urlpatterns = [
    path("", home, name="index"),
    path("update_beer/", update_beer_count, name="update_beer"),
    path("finish-session/", finish_session,
         name="finish_session"),  # Debe existir esta línea
]

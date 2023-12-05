from django.urls import path
from . import views

urlpatterns = [
    path("concert_venue/", views.get_concert_by_venue, name="concert_venue"),
    path("stats/", views.stats_view, name="stats_view"),
    path("concert_ticket/", views.get_concert_price, name="get_concert_price"),
]

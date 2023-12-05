from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, F


from tickets.models import Venue, Concert
from .utlis import colorDanger, colorPallete, \
    colorPrimary, colorSuccess, generate_color_palette


# Create your views here.


def get_concert_by_venue(request):

    concerts_by_venue = Concert.objects.values(
        'venue__name').annotate(concert_count=Count('id'))
    data = list(concerts_by_venue)
    concerts_count = [item['concert_count'] for item in data]

    venues_queryset = Venue.objects.all()

    venues_list = [venue.name for venue in venues_queryset]

    return JsonResponse({
        "title": "Concerts by Venue",
        "data": {
            "labels": venues_list,
            "datasets": [{
                "label": "Count",
                "backgroundColor": generate_color_palette(len(venues_list)),
                "borderColor": generate_color_palette(len(venues_list)),
                "data": concerts_count,
            }]
        }})


def get_concert_price(request):
    concerts_with_price = Concert.objects.annotate(concert_price=F('price'))\
        .values('name', 'concert_price')
    result_dict = {
        concert['name']: concert['concert_price'] for concert in concerts_with_price
    }

    return JsonResponse({
        "title": f"Ticket Price",
        "data": {
            "labels": list(result_dict.keys()),
            "datasets": [{
                "label": "Price",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(result_dict.values()),
            }]
        }

    })


def stats_view(request):
    return render(request, "stats.html", {})

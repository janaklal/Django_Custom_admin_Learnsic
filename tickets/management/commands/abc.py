import random
from datetime import datetime, timedelta

import pytz
from django.core.management.base import BaseCommand

from tickets.models import Venue, ConcertCategory, Concert, Ticket


class Command(BaseCommand):
    help = "Populates the database with random generated data."

    def handle(self, *args, **options):
        # populate the database with venues
        venues = [
            Venue.objects.get_or_create(
                name="NachGhar", address="Jamal, Kathmandu", capacity=960,
            ),
            Venue.objects.get_or_create(
                name="Townhall", address="Adarshanagar, Birgunj", capacity=220,
            ),
            Venue.objects.get_or_create(
                name="Jhamel Ground", address="Jhamsikhel Lalitpur", capacity=640,
            ),
            Venue.objects.get_or_create(
                name="Tiananmen square", address="Dongcheng China", capacity=12000,
            ),
            Venue.objects.get_or_create(
                name="Base Rock Cafe", address="Karachi, Pakistan", capacity=62,
            ),
        ]

        # populate the database with categories
        categories = ["Rock", "Pop", "Metal", "Hip Hop", "Jazz", "Raag"]
        for category in categories:
            ConcertCategory.objects.get_or_create(name=category)

        # populate the database with concerts
        concert_prefix = ["Underground", "Midnight",
                          "Late Night", "Secret", "Morning" * 10]
        concert_suffix = ["Party", "Rave", "Concert",
                          "Gig", "Revolution", "Jam", "Tour"]
        for i in range(10):
            venue = random.choice(venues)[0]
            category = ConcertCategory.objects.order_by("?").first()
            concert = Concert.objects.create(
                name=f"{random.choice(concert_prefix)} {category.name} {random.choice(concert_suffix)}",
                description="",
                venue=venue,
                starts_at=datetime.now(pytz.utc)
                + timedelta(days=random.randint(1, 365)),
                price=random.randint(10, 100),
            )
            concert.categories.add(category)
            concert.save()

        # populate the database with ticket purchases
        names = ["Janardhan", "John", "Rashmi", "Preeti", "Yuvi",
                 "David", "Rekha", "Joseph", "Rakesh", "Rajesh"]
        surname = ["Sharma", "Ali", "Maharjan", "Brown",
                   "Poudel", "Kapadia", "Azmat", "Deo", "Kumar", "Wagle"]
        for i in range(500):
            concert = Concert.objects.order_by("?").first()
            Ticket.objects.create(
                concert=concert,
                customer_full_name=f"{random.choice(names)} {random.choice(surname)}",
                payment_method=random.choice(
                    ["ETH", "BTC", "USDT", "SOL", "ETH", "ETH", "ETH", "BTC"]
                ),
                paid_at=datetime.now(pytz.utc) -
                timedelta(days=random.randint(1, 365)),
                is_active=random.choice([True, False]),
            )
            concert.tickets_left -= 1
            concert.save()

        self.stdout.write(self.style.SUCCESS(
            "Successfully populated the database."))

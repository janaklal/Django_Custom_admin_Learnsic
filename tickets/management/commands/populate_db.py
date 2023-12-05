import random
from datetime import datetime, timedelta
from typing import Any
import pytz
from django.core.management.base import BaseCommand
from tickets.models import Venue, Concert, ConcertCategory, Ticket


class Command(BaseCommand):
    help = "Populate the database with random generated data"

    def handle(self, *args, **options):
        # populate the datebase with venue
        venues = [Venue.objects.get_or_create(name="Bass Cafe", address="Jamal", capacity="45"),
                  Venue.objects.get_or_create(
                      name="Jawlakhel Ground", address="Jawlakhel", capacity="5000"),
                  Venue.objects.get_or_create(
                      name="Rock Cafe", address="Jamal 23", capacity="155"),
                  Venue.objects.get_or_create(
                      name="Major Stadium", address="New Ground", capacity="10000"),
                  Venue.objects.get_or_create(
                      name="NachGhar", address="Jamal 25", capacity="450"),
                  Venue.objects.get_or_create(
                      name="Coffee Ground", address="Sanepa", capacity="15"),
                  Venue.objects.get_or_create(
                      name="Town hall", address="New City", capacity="450"),

                  ]
        # populate the database with categories
        categories = ["Rock", "Pop", "Classical",
                      "Hip Hop", "Underground", "Folk"]

        for category in categories:
            ConcertCategory.objects.get_or_create(name=category)

        # Populate database with concerts
        concert_prefix = ["Underground", "Midnight", "Late Night",
                          "Evening", "Secret", "Morning", "Hot", "Cool"]
        concert_suffix = ["Party", "Rave", "Concert",
                          "Jam", "Tour", "Gig", "Revolution"]

        for i in range(20):
            venue = random.choice(venues)[0]
            category = ConcertCategory.objects.order_by("?").first()
            concert = Concert.objects.create(name=f"{random.choice(concert_prefix)}{category.name}{random.choice(concert_suffix)}",
                                             description=" ",
                                             venue=venue,
                                             starts_at=datetime.now(
                                                 pytz.utc)+timedelta(days=random.randint(1, 365)),
                                             price=random.randint(10, 100),
                                             )
            concert.categories.add(category)
            concert.save()

        # populate the database with the ticket purchase
        names = ["Rajesh", "Rakesh", "Raka", "Rojina", "Rolisha", "Rohit"]
        surname = ["Lama", "Tamang", "Rai", "Limbu", "Yadav", "Suri"]

        for i in range(500):
            concert = Concert.objects.order_by("?").first()
            print(concert)

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
            "successfully populated the database"))

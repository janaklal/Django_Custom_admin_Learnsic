from django.db import models

# Create your models here.


class Venue(models.Model):
    name = models.CharField(max_length=160)
    description = models.TextField(max_length=260, blank=True, null=True)
    address = models.CharField(max_length=256, unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"


class ConcertCategory(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=260, blank=True, null=True)

    class Meta:
        verbose_name = "concert_category"
        verbose_name_plural = 'concert categories'
        ordering = ['-name']

    def __str__(self):
        return f"{self.name}"


class Concert(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=260, blank=True, null=True)
    categories = models.ManyToManyField(ConcertCategory)
    venue = models.ForeignKey(to=Venue, on_delete=models.SET_NULL, null=True)
    starts_at = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    tickets_left = models.IntegerField(default=0)

    class Meta:
        ordering = ['starts_at']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            self.tickets_left = self.venue.capacity
        super().save(force_insert, force_update, using, update_fields)

    def is_sold_out(self):
        return self.tickets_left == 0

    def __str__(self):
        return f"{self.venue}:{self.name}"


class Ticket(models.Model):
    concert = models.ForeignKey(to=Concert, on_delete=models.CASCADE)
    customer_full_name = models.CharField(max_length=64)
    PAYMENT_METHODS = [
        ("ETH", "Ethereum"),
        ("BTC", "Bitcoin"),
        ("USDT", "Tether"),
        ("SOL", "Solana"),
    ]

    payment_method = models.CharField(
        max_length=4, default="BTC", choices=PAYMENT_METHODS)
    paid_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer_full_name}({self.concert})"


# class Ticket(models.Model):
#     concert = models.ForeignKey(to=Concert,on_delete=models.CASCADE)
#     customer_full_name = models.CharField(max_length=64)
#     PAYMENT_METHODS = [
#         ("ETH","Ethereum"),
#         ("BTC","Bitcoin"),
#         ("USDT","Tether"),
#         ("SOL","Solana"),
#     ]

#     payment_method = models.CharField(max_length=4,default="BTC",choices=PAYMENT_METHODS)
#     paid_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.customer_full_name}({self.concert})"

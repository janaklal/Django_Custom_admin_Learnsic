from typing import Any
from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin
from django.db.models.query import QuerySet

from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from djangoql.admin import DjangoQLSearchMixin

from tickets.models import Venue, ConcertCategory, Concert, Ticket
from tickets.forms import TicketAdminForm

# Register your models here.


@admin.action(description="Sold Out Ture")
def sold_out(modeladmin, request, queryset):
    queryset.update(tickets_left=0)


class ConcertInline(admin.StackedInline):
    model = Concert
    fields = ['name', "starts_at", "price", "tickets_left"]


class PoshConcert(SimpleListFilter):
    title = "Posh Concert"
    parameter_name = "posh_concert"

    def lookups(self, request, model_admin):
        return [("yes", "Yes"),
                ("no", "No")]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(price__gt=500)
        elif self.value() == "no":
            return queryset.exclude(price__gt=60)


class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "capacity"]
    inlines = [ConcertInline]


class ConcertCategoryAdmin(admin.ModelAdmin):
    pass


class ConcertAdmin(admin.ModelAdmin):
    list_display = ['name', 'starts_at',
                    'price', 'tickets_left', 'display_sold_out', 'display_venue']
    list_select_related = ['venue']
    readonly_fields = ["tickets_left"]
    # create a filter
    # list_filter = [PoshConcert]
    actions = [sold_out]

    def display_sold_out(self, obj):
        return obj.tickets_left == 0

    display_sold_out.short_description = "Sold Out"
    display_sold_out.boolean = True

    def display_venue(self, obj):
        link = reverse("admin:tickets_venue_change",
                       args=[obj.venue.id])
        return format_html('<a href="{}">{}</a>', link, obj.venue)
    display_venue.short_description = "Venue"


class TicketAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin,
                  admin.ModelAdmin):
    list_display = ["customer_full_name",
                    "concert", "payment_method", "paid_at"]
    list_select_related = ["concert", "concert__venue"]
    search_fields = ['customer_full_name', 'payment_method']

    form = TicketAdminForm


admin.site.register(Venue, VenueAdmin)
admin.site.register(ConcertCategory, ConcertCategoryAdmin)
admin.site.register(Concert, ConcertAdmin)
admin.site.register(Ticket, TicketAdmin)

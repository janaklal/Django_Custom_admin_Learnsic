from django import forms
from django.forms import ModelForm, RadioSelect

from tickets.models import Ticket


class TicketAdminForm(ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "concert", "customer_full_name", "payment_method", "is_active"
        ]

        widgets = {
            "payment_method": RadioSelect(),
        }

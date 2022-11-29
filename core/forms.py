from .models import Game
from django import forms


class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = (
            "ticket_ID",
            "booking_code",
            "odds",
            "remarks"            
        )
from chirps.models import Chirp
from django import forms
from django.forms import Textarea


class ChirpForm(forms.ModelForm):

    class Meta:
        model = Chirp
        fields = ('subject', 'message', 'image')
        widgets = {
            'message': Textarea(attrs={'rows':3, 'cols': 50})
        }

# forms.py
from django import forms
from .models import Recuerdo

class RecuerdoForm(forms.ModelForm):
    class Meta:
        model = Recuerdo
        fields = ['titulo', 'descripcion', 'imagen'] 
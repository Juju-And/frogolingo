from django import forms

from datasets.models import Expression


class ExpressionForm(forms.ModelForm):
    class Meta:
        model = Expression
        fields = ['reference', 'translation', 'image', 'sound', ]
        labels = {
            'reference': 'Wyrażenie w języku A',
            'translation': 'Wyrażenie w języku B',
            'sound': 'Dodaj nagrany dźwięk',
            'image': 'Dodaj obrazek dla skojarzeń',
        }

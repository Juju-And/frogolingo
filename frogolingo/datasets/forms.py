from django import forms

from datasets.models import Expression


class ExpressionForm(forms.ModelForm):
    class Meta:
        model = Expression
        fields = ['content']
        labels = {
            'content': 'Wyrażenie w języku A'
        }

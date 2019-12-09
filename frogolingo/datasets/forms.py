from django import forms

from datasets.models import Expression


class ExpressionForm(forms.ModelForm):
    class Meta:
        model = Expression
        fields = ['content', 'sound']
        labels = {
            'content': 'Wyrażenie w języku A'
        }


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
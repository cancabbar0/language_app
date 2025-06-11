from django import forms
from .models import Words


class WordsForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = ['english', 'turkish', 'in_sentence', 'img']

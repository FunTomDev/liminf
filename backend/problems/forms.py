from django import forms

from .models import Problem

class ProblemForm(forms.ModelForm):
    """Form for creating and updating problems"""
    class Meta:
        model = Problem
        fields = ['title', 'description', 'topic', 'content', 'file']
        labels = {
            'title': 'Tutuł',
            'description': 'Opis',
            'topic': 'Temat',
            'content': 'Treść (opcjonalnie, jeśli załączono plik)',
            'file': 'Plik (opcjonalnie, jeśli dodano treść)',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 30, 'cols': 90}),
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }
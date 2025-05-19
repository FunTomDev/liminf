from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    """Form for creating and updating materials"""
    class Meta:
        model = Material
        fields = ['title', 'description', 'content', 'file', 'topic']
        labels = {
            'title': 'Tutuł',
            'description': 'Opis',
            'content': 'Treść (opcjonalnie, jeśli załączono plik)',
            'file': 'Plik (opcjonalnie, jeśli dodano treść)',
            'topic': 'Temat',
        }
        widgets = {
            'content': forms.Textarea(attrs={'cols': 120, 'rows': 40, 'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }
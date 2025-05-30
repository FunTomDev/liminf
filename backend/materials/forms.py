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
            'topic': 'Temat',
            'content': 'Treść (opcjonalnie, jeśli załączono plik)',
            'file': 'Plik (opcjonalnie, jeśli dodano treść)',
        }
        widgets = {
            'content': forms.Textarea(attrs={'cols': 120, 'rows': 10, 'class': 'w-full'}),
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        file = cleaned_data.get('file')

        if not content and not file:
            raise forms.ValidationError("Materiały muszą mieć treść albo załączony plik.")
        return cleaned_data
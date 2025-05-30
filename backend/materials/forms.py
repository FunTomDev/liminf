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
        if file and not file.name.lower().endswith(('.pdf')):
            raise forms.ValidationError("Aktualnie obsługiwane są tylko pojedyńcze pliki PDF. Jest to ograniczenie związane z brakiem czasu na zabawę z obsługą wielu formatów. Pls don't kill me 🙏😭")
        if file and len(file.name) > 600:
            raise forms.ValidationError("Nazwa pliku jest zbyt długa. Maksymalna długość to 512 znaków.")
        return cleaned_data
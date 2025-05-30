from django import forms

from .models import Solution

class SolutionForm(forms.ModelForm):
    """Form for creating and updating solutions"""
    class Meta:
        model = Solution
        fields = ['title', 'description', 'content', 'file']
        labels = {
            'title': 'Tytuł',
            'description': 'Opis',
            'content': 'Treść (opcjonalnie, jeśli załączono plik)',
            'file': 'Plik (opcjonalnie, jeśli dodano treść)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 90, 'class': 'w-full'}),
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        file = cleaned_data.get('file')

        if not content and not file:
            raise forms.ValidationError("Rozwiązanie musi zawierać treść albo załączony plik.")
        return cleaned_data

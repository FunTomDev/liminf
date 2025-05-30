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
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 90, 'class': 'w-full'}),
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned data:", cleaned_data)
        content = cleaned_data.get('content')
        file = cleaned_data.get('file')

        if not content and not file:
            raise forms.ValidationError("Zadania muszą mieć treść albo załączony plik.")
        return cleaned_data
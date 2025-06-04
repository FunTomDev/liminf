from django import forms

from .models import Solution

class SolutionForm(forms.ModelForm):
    """Form for creating and updating solutions"""

    clear_file = forms.BooleanField(
        label="Usuń plik",
        required=False,
    )
    class Meta:
        model = Solution
        fields = ['title', 'description', 'content', 'file']
        labels = {
            'title': 'Tytuł',
            'description': 'Opis',
            'content': 'Treść',
            'file': 'Plik',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 90, 'class': 'hidden'}),
            'file': forms.FileInput(attrs={'multiple': False}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        file = cleaned_data.get('file')
        clear_file = cleaned_data.get('clear_file')

        # Check if a file will exist after save
        has_existing_file = bool(self.instance and self.instance.file and not clear_file)
        has_uploaded_file = 'file' in self.files

        if not content and not (has_uploaded_file or has_existing_file):
            raise forms.ValidationError(
                "Rozwiazania muszą mieć treść albo załączony plik."
            )

        if file:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError(
                    "Aktualnie obsługiwane są tylko pojedyńcze pliki PDF. Jest to ograniczenie związane z brakiem czasu na zabawę z obsługą wielu formatów. Pls don't kill me 🙏😭"
                )
            if len(file.name) > 600:
                raise forms.ValidationError(
                    "Nazwa pliku jest zbyt długa. Maksymalna długość to 512 znaków."
                )

        return cleaned_data

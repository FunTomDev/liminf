from django import forms

from .models import Problem

class ProblemForm(forms.ModelForm):
    """Form for creating and updating problems"""

    clear_file = forms.BooleanField(
        label="Usuń plik",
        required=False,
    )
    class Meta:

        model = Problem
        fields = ['title', 'description', 'topic', 'content', 'file']
        labels = {
            'title': 'Tutuł',
            'description': 'Opis',
            'topic': 'Temat',
            'content': 'Treść',
            'file': 'Plik',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 90, 'class': 'hidden'}),
            'file': forms.FileInput(attrs={'multiple': False}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
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
                "Zadania muszą mieć treść albo załączony plik."
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
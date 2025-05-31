from django import forms

from curriculum.models import Subject, Topic, Semester

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'semester']
        labels = {
            'name': 'Nazwa przedmiotu',
            'semester': 'Semestr',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa przedmiotu'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'name']
        labels = {
            'subject': 'Przedmiot',
            'name': 'Nazwa tematu',
        }
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa tematu'}),
        }
from django import forms

from curriculum.models import Subject, Topic, Semester

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        labels = {
            'name': 'Nazwa przedmiotu',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa przedmiotu'}),
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
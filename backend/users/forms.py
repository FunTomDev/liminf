from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User

class StudentCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2')
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'username': 'Login',
            'email': 'Email',
            'password1': 'Hasło',
            'password2': 'Powtórz hasło'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Login',
            'password': 'Hasło'
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'account_type', 'bio')
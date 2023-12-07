from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'autofocus': True}),
    )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    username = forms.CharField(label="Username", required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")  # Include the fields you need

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email"
        self.fields['username'].label = "Username"

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from collections import UserList
from django import forms
from .models import Profile, UserProfile
from django.contrib.auth import get_user_model

from authentication.models import UserProfile


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate', 'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist!")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password!")
            if not user.is_active:
                raise forms.ValidationError("This user is not active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(
        label='Password confirmation',
        help_text='Enter the same password as before, for verification.',
        widget=forms.PasswordInput(attrs={'placeholder': 'Re Enter Password'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'profile_picture')



class ArtistSignupForm(forms.Form):
    """Form for artist signup, capturing necessary artist information."""

    username = forms.CharField(
        label="Username",
        max_length=30,
        help_text="A unique username for logging in.",
        required=True,
    )
    artist_name = forms.CharField(
        label="Artist Name",
        max_length=50,
        help_text="Your Names",
        required=True,
    )
    stage_name = forms.CharField(
        label="Stage Name",
        max_length=50,
        help_text="The name you'd like to be known by as an artist.",
        required=True,
    )
    email = forms.EmailField(
        label="Email",
        help_text="A valid email address for communication.",
        required=True,
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,  # Use password masking for security
        help_text="A strong password is recommended (at least 8 characters with a mix of letters, numbers, and symbols).",
        required=True,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,  # Use password masking for security
        help_text="Enter the same password as above.",
        required=True,
    )

    def clean_password2(self):
        """Ensures both password fields match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2

    def clean_email(self):
        """Validates uniqueness of email address."""
        User = get_user_model()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def save(self):
        """Create a new user (artist) and save their information."""
        User = get_user_model()
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        # Additional logic to save artist-specific information (e.g., artist_name, stage_name)
        # You can create an Artist model and associate it with the user here.
        # Example: artist = Artist.objects.create(user=user, artist_name=self.cleaned_data['artist_name'])
        return user   


  
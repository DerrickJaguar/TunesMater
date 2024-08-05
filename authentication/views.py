from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authentication.models import Artist, UserProfile
from .forms import ArtistSignupForm, UserLoginForm, RegistrationForm, UserProfileForm 
from django.contrib.auth.models import User
from .models import Profile



# Create your views here.
def login_request(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    context = {
        'form': form,
        'title': title,
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        login(request, user)
        # messages.info(request, f"You are now logged in  as {user}")
        return redirect('index')
    else:
        print(form.errors)
        # messages.error(request, 'Username or Password is Incorrect! ')
    return render(request, 'authentication/login.html', context=context)


def signup_request(request):
    title = "Create Account"
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': title}
    return render(request, 'authentication/signup.html', context=context)


def logout_request(request):
    logout(request)
    #messages.info(request, "Logged out successfully!")
    return redirect('index')

def artist_signup(request):
  if request.method == 'POST':
    form = ArtistSignupForm(request.POST)
    if form.is_valid():
      # Using ModelForm (if applicable):
      user = form.save()  # This saves the user and returns the created User object

      # Additional actions for artist profile (if not using ModelForm):
      profile = Profile.objects.create(user=user,)  # Create a profile object for the user
      profile.stage_name = form.cleaned_data['stage_name']
      profile.artist_name = form.cleaned_data['artist_name']
         # ... save other artist profile details
      profile.save()

      return redirect('authentication/login.html')  # Replace with your success URL pattern name
  else:
    form = ArtistSignupForm()

  context = {'form': form}
  return render(request, 'authentication/artist_signup.html', context)


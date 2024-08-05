from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    UserProfiler = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_profile')
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)  # You might want to use a more secure way to store passwords
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username
# artists/models.py

class Artist(models.Model):
    Artist_Name = models.CharField(max_length=100, default='Edrisa Musuza')
    Stage_Name = models.CharField(max_length=100, default='Eddy Kenzo')
    Username = models.CharField(max_length=50, unique=True, default='eddy')
    Email = models.EmailField(unique=True, default='derrric65@gmail.com')  # Set your desired default email
    Password = models.CharField(max_length=128, default='nakacwa123')  # Store hashed passwords

    def __str__(self):
        return self.Artist_Name
  
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  # Artist-specific fields (optional)
  stage_name = models.CharField(max_length=50, blank=True)
  genre = models.CharField(max_length=50, blank=True)
  bio = models.TextField(blank=True)

  # Listener-specific fields (optional)
  display_name = models.CharField(max_length=50, blank=True)
  country = models.CharField(max_length=50, blank=True)

  # Notification settings (common)
  notify_emails = models.BooleanField(default=True)
  notify_in_app = models.BooleanField(default=True)

  # Privacy settings (common)
  public_profile = models.BooleanField(default=True)
  show_activity = models.BooleanField(default=True)

  # Playback settings (common)
  audio_quality = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')

  def __str__(self):
    return self.user.username
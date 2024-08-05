from collections import UserList
from django import forms
from .models import UploadedFile, UserProfile

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'mp3_file']
class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['stage_name', 'genre', 'bio', 'display_name', 'country',
                  'notify_emails', 'notify_in_app', 'public_profile',
                  'show_activity', 'audio_quality']    

       
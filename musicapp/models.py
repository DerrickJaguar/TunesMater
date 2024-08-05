from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class Song(models.Model):

    Language_Choice = (
              ('Local', 'Local'),
              ('English', 'English'),
          )

    name = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    language = models.CharField(max_length=20,choices=Language_Choice,default='English')
    song_img = models.FileField()
    year = models.IntegerField()
    singer = models.CharField(max_length=200)
    song_file = models.FileField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)



from django.db import models

class Settings(models.Model):
    stage_name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    bio = models.TextField()
    display_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notify_emails = models.EmailField(blank=True, null=True)
    notify_in_app = models.BooleanField(default=False)
    public_profile = models.BooleanField(default=False)
    show_activity = models.BooleanField(default=False)
    audio_quality = models.IntegerField(default=128)

    def __str__(self):
        return self.stage_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    bio = models.TextField()
    display_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    notify_emails = models.BooleanField(default=True)
    notify_in_app = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=True)
    show_activity = models.BooleanField(default=True)
    audio_quality = models.CharField(max_length=255)

    def __str__(self):
        return self.stage_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class UploadedFile(models.Model):
    title = models.CharField(max_length=100)
    mp3_file = models.FileField(upload_to='Songs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.mp3_file.delete()  
        super().delete(*args, **kwargs)

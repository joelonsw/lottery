from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=30, blank=False)
    location = models.CharField(max_length=30, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=100, blank=False)
    address_detail = models.CharField(max_length=100, blank=False)
    # 위도, 경도 초기화를 위해 넣었습니다. -현준-
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
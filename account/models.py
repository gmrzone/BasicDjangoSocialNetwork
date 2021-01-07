from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
import datetime
import pytz
import os
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Create your models here.
def get_image_path(instance, filename):
    name = instance.user.username
    time = pytz.utc.localize(datetime.datetime.utcnow())
    return os.path.join(name, time.strftime('%Y'), time.strftime('%m'), time.strftime('%d'), filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(verbose_name='Profile Slug', unique_for_date='updated', max_length=60, null=True)
    photo = models.ImageField(upload_to=get_image_path, default='default_profile.png')
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        absolute_url = reverse('profile', args=[self.id, self.slug])
        return absolute_url

    def get_absolute_url_update(self):
        absolute_url = reverse('update_profile', args=[self.id, self.slug])
        return absolute_url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
            super().save(*args, **kwargs)

    def __str__(self):
        return 'Profile For User {0}'.format(self.user.username)

# Intermidiary Model for Follow System

class FollowIntermidiary(models.Model):
    user_from = models.ForeignKey('auth.user', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.user', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "{0} following {1}".format(self._from, self._to)

# Adding new field to user model using models.add_to_class method first get user model using get_user_model

user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self', related_name='followers', through=FollowIntermidiary, symmetrical=False))

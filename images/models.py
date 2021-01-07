from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
import os
from django.utils import timezone
from django.shortcuts import reverse

def get_username(instance, filename):
    # username = instance.user.username
    username = 'Image_bookmark'
    date = timezone.now()
    dir = os.path.join(username, 'Image_uploads', date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), filename)
    return dir
# Create your models here.


class ImagePost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='image_post', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, verbose_name='Title')
    description = models.TextField(max_length=800, verbose_name='Description', null=True)
    slug = models.SlugField(max_length=50,  blank=True, db_index=True, unique_for_date='created')
    url = models.URLField()
    image = models.ImageField(upload_to=get_username)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='image_likes', blank=True)
    like_count = models.PositiveIntegerField(default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse('post_detail', args=(self.slug, self.created.year, self.created.month, self.created.day))
        return url

    def __str__(self):
        return self.title   
from django.db.models.signals import m2m_changed
from .models import ImagePost
from django.dispatch import receiver


@receiver(m2m_changed, sender=ImagePost.users_like.through)
def user_likes_changed(sender, instance, **kwargs):
    instance.like_count = instance.users_like.count()
    instance.save()
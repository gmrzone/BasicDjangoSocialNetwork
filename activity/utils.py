#  This file contains function to be used by view.py file
from .models import UserActivity
import datetime
from django.utils import timezone
from .models import UserActivity
from django.contrib.contenttypes.models import ContentType


def create_activity(user, action, target=None):
    # Before Creating activity we will check if the same activity already exist to avoin duplicate activity
    # getting all user activity in the last minute. here we are getting all activity of user with similar action as the activity we have to create example User x follows.
    # we still have to filter target so that we can detect duplicate activity like userx follows usery
    current_time = timezone.now()
    last_minute = current_time - datetime.timedelta(seconds=10)
    similar_activity = UserActivity.objects.filter(user=user, action=action, created__gte=last_minute)
    if target:
        target_contenttype = ContentType.objects.get_for_model(target)
        similar_activity = similar_activity.filter(user=user, target_ct=target_contenttype, target_id=target.id)

    if not similar_activity:
        UserActivity.objects.create(user=user, action=action, target=target)
        return True
    return False

def remove_activity(user, action, target=None):
    pass

    # if target is not None filter again to only include activity with same target in similar activity 





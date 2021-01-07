from django.shortcuts import render
from django.http import HttpResponse
from .models import UserActivity

# Create your views here.


def activity_stream(request):
    # Getting All Activities Except activities of request.user
    activity_list = UserActivity.objects.all().exclude(user=request.user).select_related('user', 'user__profile').prefetch_related('target')
    # Get id of user whom request.user is following so we can filter their activities
    following_id = request.user.following.values_list('id', flat=True)
    if following_id:
        activity_list = activity_list.filter(user__in=following_id)
    context = {'activities': activity_list}
    return render(request, 'activities.html', context=context)
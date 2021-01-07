from django.shortcuts import render
from .forms import ImagePostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ImagePost
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .decorators import ajax_only
from activity.utils import create_activity
# Redis Imports
import redis
from django.conf import settings
# Create your views here.

# Establishing a redis Connection

redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required(login_url='login')
def image_post(request):
    if request.method == 'POST':
        print(request.POST)
        image_form = ImagePostForm(data=request.POST)
        if image_form.is_valid():
            img_obj = image_form.save(commit=False)
            img_obj.user = request.user
            img_obj.save()
            create_activity(request.user, "Bookmarked", img_obj)
            messages.success(request, 'Image Added Sucessfully')
    else:
        # Built Form with dataprovided by bookmarklet javascript via GET
        image_form = ImagePostForm(data=request.GET)
        print(request.GET)

    context = {'image_form': image_form, 'section': 'images'}
    return render(request, 'images/create_image_post.html', context)


def post_detail(request, slug, year, month, day):
    selected_post = get_object_or_404(ImagePost, slug=slug, created__year=year, created__month=month, created__day=day)
    # INCREMENT Image Ranking for top posts using zincrby which will create a set with name imagerank
    redis_conn.zincrby('imagerank', 1, selected_post.id)
    post_views = redis_conn.incr(f'image:{selected_post.id}:views')
    context = {'selected_post': selected_post, 'post_views': post_views}
    return render(request, 'images/post_detail.html', context)
 
    
@ajax_only
@require_POST
@login_required(login_url='login')
def like_image(request):
    id = request.POST.get('post_id')
    selected_post = get_object_or_404(ImagePost, pk=id)
    user = request.user
    if user in selected_post.users_like.all():
        selected_post.users_like.remove(user)
        create_activity(request.user, "Unliked", selected_post)
        data = {'action': 'like'}
    else:
        selected_post.users_like.add(user)
        create_activity(request.user, "Liked", selected_post)
        data = {'action': 'unlike'}
    return JsonResponse(data)
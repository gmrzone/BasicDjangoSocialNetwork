from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginUSer, CreateUser, CreateNewUser, ProfileForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import login_required # login, logout view and login_required Decorator
from django import forms
from .models import Profile, FollowIntermidiary
from images.models import ImagePost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from images.decorators import ajax_only
from activity.utils import create_activity

# redis nection
import redis
from django.conf import settings
redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# Create your views here.

@login_required(redirect_field_name='login')
@require_POST
@ajax_only
def follow_user(request):
    following_user = request.user
    user_id = request.POST.get('user_id', False)
    follow_user = get_object_or_404(User, pk=user_id)
    if following_user in follow_user.followers.all():
        inetrmidairy_model = FollowIntermidiary.objects.get(user_from=following_user, user_to=follow_user)
        inetrmidairy_model.delete()
        create_activity(request.user, "Unfollows", follow_user)
        data = {'msg': "Follow"}
    else:
        inetrmidairy_model = FollowIntermidiary.objects.get_or_create(user_from=following_user, user_to=follow_user)
        data = {'msg': "Unfollow"}
        create_activity(request.user, "is Following", follow_user)
    return JsonResponse(data)



def login_user(request):
    if request.method == "POST":
        login_form = LoginUSer(request.POST)
        if login_form.is_valid():
            login_details = login_form.cleaned_data
            user = authenticate(request,username=login_details['username'], password=login_details['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Your Account Has Been Disabled For Security Reasons.')
            else:
                messages.warning(request, 'Invalid Username or Password. Please Try Again.')
    else:
        login_form = LoginUSer()
    context = {'login_form': login_form}
    return render(request, 'login_and_signup/login.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        redirect('login')
    return redirect('home')

# Custom USer Creation Form
def create_user(request):
    if request.method == 'POST':
        signup_form = CreateUser(request.POST)
        if signup_form.is_valid():
            try:
                validate_password = signup_form.cleaned_password()
            except forms.ValidationError:
                messages.error(request, 'Both Password Dont match')
            else:
                new_user = signup_form.save(commit=False)
                new_user.set_password(validate_password)
                new_user.save()
                create_activity(new_user, "Created Account")
                messages.success(request, "Your Account Was Sucessfully Created. You Can Login Now")
                # # Using signals instead
                # user_profile = Profile()
                # user_profile.user = new_user
                # user_profile.slug = new_user.username
                # user_profile.save()
                return redirect('login')
    else:
        signup_form = CreateUser()
    context = {'signup_form': signup_form}
    return render(request, 'login_and_signup/signup.html', context)

# Django Default USer Creation Form
def user_creation(request):
    if request.method == "POST":
        signup_form = CreateNewUser(request.POST)
        if signup_form.is_valid():
            new_user = signup_form.save()
            # Profile.objects.create(user=new_user, slug= new_user.username) # Using signals instead
            messages.success(request, "Your Account Was Sucessfully Created. You Can Login Now")
            return redirect('login')

    else:
        signup_form = CreateNewUser()
    context = {'signup_form': signup_form}
    return render(request, 'login_and_signup/signup.html', context)

@login_required(login_url='login')
def home(request):
    post_list = ImagePost.objects.all().order_by('-created').select_related('user', 'user__profile')
    paginator = Paginator(post_list, 8)
    current_page = request.GET.get('page')
    most_viewed = redis_conn.zrange('imagerank', 0, -1, desc=True)[:5]
    most_viewrd_id = [int(id) for id in most_viewed]
    most_viewed_post = list(post_list.filter(id__in=most_viewrd_id))
    most_viewed_post.sort(key=lambda x : most_viewrd_id.index(x.id))
    try:
        post_list = paginator.page(current_page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        # this will help stop ajax pagination on client side when page is empty
        if request.is_ajax():
            return HttpResponse('')
        else:
            post_list = paginator.page(paginator.num_pages)
    context = {'section' : 'home', 'image_posts': post_list}
    if request.is_ajax():
        return render(request, 'home/ajax_post_list.html', context)
    else:
        context.update({'most_viewed_post': most_viewed_post})
        return render(request, 'home/home.html', context)

@login_required(login_url='login')
def profile(request, id, slug):
    section = 'profile'
    selected_profile = Profile.objects.select_related('user').prefetch_related('user__following', 'user__followers', 'user__image_post').get(id=id, slug=slug)
    context = {'selected_profile': selected_profile, 'section': section}
    return render(request, 'profile/profile.html', context)

def profile_list(request):
    section = 'users'
    all_users = User.objects.filter(is_active=True).select_related('profile')
    
    context = {'section': section, 'all_user': all_users}
    return render(request, 'profile/profile_list.html', context)
    
@login_required(login_url='login')
def update_profile(request, id, slug):
    selected_profile = get_object_or_404(Profile, id=id, slug=slug)
    selected_user = selected_profile.user
    if request.method == 'POST':
        profile_form = ProfileForm(instance=selected_profile, data=request.POST, files=request.FILES)
        user_form = UserForm(instance=selected_user, data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            new_user = user_form.save()
            if new_user.username != selected_profile.slug:
                selected_profile.slug = new_user.username
                selected_profile.save()
            messages.success(request, 'Your Profile was Sucessfully Updated')
        else:
            messages.error(request, 'There Was Some Problem Updating Your Profile Please Try Again Later.')
    else:
        profile_form = ProfileForm(instance=selected_profile)
        user_form = UserForm(instance=selected_user)
    context = {'profile_form': profile_form, 'user_form': user_form, 'selected_user': selected_user}
    return render(request, 'profile/profile_update.html', context)


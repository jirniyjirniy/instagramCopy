from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from authy.models import Profile
from post.models import Post, Follow, Stream
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from django.core.paginator import Paginator


def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favorites.all()

    # Profile info
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()

    # Follow status
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # Posts likes
    if posts.exists():
        posts_likes = posts.aggregate(Sum('likes'))['likes__sum']
    else:
        posts_likes = 0

    # Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    template = loader.get_template('profile.html')

    context = {
        'posts': posts_paginator,
        'profile': profile,
        'url_name': url_name,
        'posts_count': posts_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'follow_status': follow_status,
        'posts_likes': posts_likes
    }

    return render(request, 'profile.html', context)


def UserProfileFavorites(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    posts = profile.favorites.all()

    # Profile info box
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()

    # Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    template = loader.get_template('profile_favorite.html')

    context = {
        'posts': posts_paginator,
        'profile': profile,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_count': posts_count,
    }

    return HttpResponse(template.render(context, request))


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'change_password.html', context)


def PasswordChangeDone(request):
    return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
    user = request.user.id
    user_info = Profile.objects.filter(user=user)
    profile = Profile.objects.get(user__id=user)
    BASE_WIDTH = 400

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('picture'):
                profile.picture = form.cleaned_data.get('picture')
            if form.cleaned_data.get('first_name'):
                profile.first_name = form.cleaned_data.get('first_name')
            if form.cleaned_data.get('last_name'):
                profile.last_name = form.cleaned_data.get('last_name')
            if form.cleaned_data.get('location'):
                profile.location = form.cleaned_data.get('location')
            if form.cleaned_data.get('url'):
                profile.url = form.cleaned_data.get('url')
            if form.cleaned_data.get('profile_info'):
                profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('index')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
        'user_info': user_info,
    }

    return render(request, 'profile_edit.html', context)


@login_required
def follow(request, username, option):
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()

        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))

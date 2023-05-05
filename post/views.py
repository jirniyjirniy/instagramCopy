from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from authy.models import Profile
from post.forms import PostForm
from post.models import Post, Stream, Tag, Likes


@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    group_ids = [post.post_id for post in posts]

    post_items = Post.objects.filter(id__in=group_ids).select_related('user__profile').all().order_by('-posted')
    liked_posts = [like.post_id for like in Likes.objects.filter(user=user)]
    favorite_posts = [post.id for post in Profile.objects.get(user=user).favorites.all()]

    template = loader.get_template('index.html')

    context = {
        'post_items': post_items,
        'liked_posts': liked_posts,
        'favorite_posts': favorite_posts
    }

    return HttpResponse(template.render(context, request))


@login_required
def new_post(request):
    user = request.user.id
    tags_obj = []

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags = form.cleaned_data.get('tags')
            tags_list = list(tags.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)

            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('index')
    else:
        form = PostForm()

    context = {
        'form': form,
    }

    return render(request, 'upload_post.html', context)

@login_required
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    user_obj = Profile.objects.get(user=user)

    template = loader.get_template('post_detail.html')

    liked = Likes.objects.filter(user=user, post=post).exists()
    favorite_post = Profile.objects.get(user=user).favorites.filter(id=post_id).exists()

    context = {
        'post': post,
        'user_obj': user_obj,
        'post_id': post_id,
        'liked': liked,
        'favorite_post': favorite_post
    }

    return HttpResponse(template.render(context, request))


@login_required
def tag_page(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    template = loader.get_template('tag.html')

    context = {
        'tag': tag,
        'posts': posts,
    }

    return HttpResponse(template.render(context, request))


@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes += 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('post_details', args=[post_id]))

@login_required
def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    favorite_post = profile.favorites.filter(id=post_id).exists()

    if favorite_post:
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)

    return HttpResponseRedirect(reverse('post_details', args=[post_id]))
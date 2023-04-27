from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse

from authy.models import Profile
from post.forms import PostForm
from post.models import Post, Stream, Tag


@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    group_ids = [post.post_id for post in posts]

    post_items = Post.objects.filter(id__in=group_ids).select_related('user__profile').all().order_by('-posted')


    template = loader.get_template('index.html')

    context = {
        'post_items': post_items,

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

    context = {
        'post': post,
        'user_obj': user_obj,
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
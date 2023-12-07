from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request, id):
    try:
        post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    except Post.DoesNotExist:
        raise Http404('No post found')
    return render(request, 'blog/post/detail.html', {'post': post})

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from django.http import Http404


def index(request):
    now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    now = timezone.now()
    post = get_object_or_404(Post, pk=id)

    if (post.pub_date > now or not post.is_published or not
            post.category.is_published):
        raise Http404

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    now = timezone.now()
    category = get_object_or_404(Category, slug=category_slug)

    if not category.is_published:
        raise Http404

    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=now,
    ).order_by('-pub_date')

    context = {'category': category, 'post_list': posts}
    return render(request, 'blog/category.html', context)

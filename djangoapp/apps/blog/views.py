from django.core.paginator import Paginator
from django.shortcuts import render
from apps.blog.models import Post, Page
from django.db.models import Q

PER_PAGE = 9


def index(request):
    posts = Post.objManager.get_published().order_by('-pk')

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def created_by(request, author_pk):
    posts = Post.objManager.get_published()\
        .filter(created_by__pk=author_pk)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug):
    posts = Post.objManager.get_published()\
        .filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def page(request, slug):
    page = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page,
        }
    )


def post(request, slug):
    post = Post.objManager.get_published().filter(slug=slug).first()
    
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )
    
def tag(request, slug):
    posts = Post.objManager.get_published()\
        .filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )
    
def search(request):
    search_value = request.GET.get('search', '').strip()

    posts = (
        Post.objManager.get_published()
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]
    )

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
        }
    )
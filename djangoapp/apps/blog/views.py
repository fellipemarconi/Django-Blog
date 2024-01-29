from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render
from apps.blog.models import Post, Page
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.models import User
from django.views.generic import ListView

PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objManager.get_published()
    
    # If I want to mess with queryset
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - ',
        })
        
        return context

class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        context.update({
            'page_title': page_title,
        })

        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by__pk=self._temp_context['user'].pk)
        return queryset

class CategoryListView(PostListView):
    allow_empty = False
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Categoria - ' #type: ignore
        context.update({
            'page_title': page_title,
        })
        return context
    
def page(request, slug):
    page_obj = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


def post(request, slug):
    post_obj = (
        Post.objManager.get_published()
        .filter(slug=slug)
        .first()
    )

    if post_obj is None:
        raise Http404()

    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
    
def tag(request, slug):
    posts = Post.objManager.get_published()\
        .filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    page_title = f'{page_obj[0].tags.first().name} - Tag - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
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

    
    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )
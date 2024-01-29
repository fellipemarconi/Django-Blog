from django.urls import path
from apps.blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', views.post, name='post'),
    path('page/<slug:slug>/', views.page, name='page'),
    path('created_by/<int:author_pk>/', views.CreatedByListView.as_view(), 
         name='created_by'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagListView.as_view(), name='tag'),
    path('search/', views.search, name='search'),
]
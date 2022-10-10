from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [


    path('list/', views.article_list, name='article-list'),
    path('<slug:slug>', views.article_detail, name='article-detail'),
    path('category/list/', views.category_list, name='category-list'),
    path('category/create/', views.category_create, name='category-create'),
    path('category/<int:pk>', views.category_detail, name='category-detail'),
    path('create/', views.article_create, name='article-create'),
    path('update/<slug:slug>', views.article_update, name='article-update'),
    path('delete/<slug:slug>', views.article_delete, name='article-delete'),
    path('search/', views.article_search, name='article-search'),
    path('comment/delete/<int:id>', views.comment_delete, name='comment-delete'),
    path('comment/update/<int:id>', views.comment_update, name='comment-update'),
]

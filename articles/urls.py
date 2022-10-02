from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [

   
    path('list/',views.list_try,name='article-list'),
    path('<slug:slug>',views.detail_try,name='article-detail'),
    path('create/',views.create_try,name='article-create'),
    path('update/<slug:slug>',views.update_try,name='article-update'),
    path('delete/<slug:slug>',views.delete_try,name='article-delete'),
    path('search/',views.qs_search,name='article-search'),
    path('comment/delete/<int:id>',views.comment_delete,name='delete_comment'),
]
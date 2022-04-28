from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [

    path('',views.list_try,name='list_view'),
    path('<slug:slug>',views.detail_try,name='detail_view'),
    path('create/',views.create_try,name='create_article'),
    path('update/<slug:slug>',views.update_try,name='update_article'),
    path('delete/<slug:slug>',views.delete_try,name='delete_article'),

    # path('',views.list_view,name='list_view'),
    path('search/',views.qs_search,name='search'),
    path('<int:id>',views.detail_view,name='detail_view'),
    # path('create/',views.create_article,name='create_article'),
    path('update/<int:id>',views.update_view,name='update_article'),
    path('comment/delete/<int:id>',views.comment_delete,name='delete_comment'),
]
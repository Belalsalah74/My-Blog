from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/<int:id>/', views.profile_view, name='profile'),
    path('profile/update/<int:id>/', views.udpate_profile, name='profile_update'),
    path('user/<int:id>/password/', views.PassChange, name='password_change'),
]

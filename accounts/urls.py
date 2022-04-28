from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('login/',views.login_try,name='login'),
    # path('login/',views.login_view,name='login'),
    path('logout/',views.logout_try,name='logout'),
    # path('logout/',views.logout_view,name='logout'),
    path('register/',views.register_try,name='register'),
    # path('register/',views.register_view,name='register'),
    path('profile/<int:id>/',views.profile_view,name='profile'),
    path('profile/update/<int:id>/',views.udpate_profile,name='profile_update'),
    path('password/<int:id>/',views.PassChange,name='password_change'),
]
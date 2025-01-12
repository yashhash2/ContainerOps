from django.contrib import admin
from django.urls import path, include
from . import views

app_name="api"
urlpatterns = [
    
    path('signup/', views.createUser, name="signup"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('get_url/', views.get_url, name='get_url'),
    path('deploy/', views.run, name='deploy'),
]

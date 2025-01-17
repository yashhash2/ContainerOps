from django.contrib import admin
from django.urls import path, include
from . import views

app_name="api"
urlpatterns = [
    
    path('signup/', views.create_user, name="signup"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('fetch_giturl/', views.fetch_giturl, name='fetch_giturl'),
    path('deploy/', views.run, name='deploy'),
]

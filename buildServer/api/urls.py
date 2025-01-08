from django.contrib import admin
from django.urls import path
import views


urlpatterns = [
    path('run/',views.run,name="run")
]

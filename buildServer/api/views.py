from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse ,HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import docker
import os
from .models import User
# DEPLOYMENTS
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'home.html')
        
        else:
            username = request.POST.get('username')
            if not User.objects.filter(username=username).exists():
                # Redirect to signup page
                return redirect('api:signup')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def createUser(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            
            # redirect to login page
            request.session['signup_success'] = True
            return redirect('api:login')

    
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')
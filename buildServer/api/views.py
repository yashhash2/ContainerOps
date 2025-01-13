from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



from .forms import SignupForm

import requests
import json
import docker
import os

from .models import User, Deployments


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
    return redirect('/')

def run(request):
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                body = json.loads(request.body)
                github_url = body.get("githubUrl")
                user_uid = body.get("user_id")
               
            else:
                github_url = request.POST.get("githubUrl")
                user = request.user
                username = user.username
                user_uid = user.uid
             
            
            docker_user = os.getenv("DOCKER_USERNAME")
            docker_pass = os.getenv("DOCKER_PASSWORD")
            image_name = os.getenv("IMAGE_NAME")
            cmd = os.getenv("CMD")
            env_content = os.getenv("ENV_CONTENT", "")

            # Validate required parameters
            if not all([github_url, docker_user, docker_pass, image_name, username, user_uid]):
                logger.error("Missing required parameters.")
                return JsonResponse({"status": "error", "message": "Missing required parameters."})
            
            try:
                user = User.objects.get(uid=user_uid)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            

            # Clone repository, build, and push image
            client = docker.from_env()
  
            # build the image manually using docker build -t final_deploy . (before calling the run fn)
            container = client.containers.run(
                image='final_deploy',
                detach=True,
                environment={
                    "GIT_URL": github_url,
                    "DOCKER_USERNAME": docker_user,
                    "DOCKER_PASSWORD": docker_pass,
                    "IMAGE_NAME": image_name,
                },
                volumes={"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}},
                privileged=True,
            )

            # Stream logs
            logs = container.logs(stream=True)
            logs_output = ""
            for log in logs:
                decoded_log = log.decode("utf-8")
                logs_output += decoded_log
        
            container.stop()
            container.remove()
            #hit a URL to show success:url:http://172.25.96.1:8001/api/webhook,request type:POST,req.body:{id,image_name,image_port}
            payload = {
                "id": container.id,
                "image_name": image_name,
                "image_port": "3000"
            }
            
            try:
                webhook_url = "http://localhost:8001/api/webhook/"
                response = requests.post(webhook_url, json=payload)
                print(response.json())
            except Exception as e:
                print(f"Failed to hit webhook URL: {str(e)}")
            
            return JsonResponse({
                "status": "success",
                "message": "Container executed successfully.",
                "containerId": container.id,
            })

        except Exception as e:
           return JsonResponse({
                "status": "error",
                "message": "Failed to execute container.",
                "error": str(e),
            })

    return JsonResponse({"status": "error", "message": "Invalid request method. Use POST."})


@login_required
def get_url(request):
    return render(request, 'get_url.html')
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


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

@csrf_exempt
def run(request):
    if request.method == "POST":
        try:
            # Parse the JSON request body
            body = json.loads(request.body)
            github_url = body.get("githubUrl", None)
            docker_user = os.getenv("DOCKER_USERNAME")
            docker_pass = os.getenv("DOCKER_PASSWORD")
            image_name = os.getenv("IMAGE_NAME")
            cmd = os.getenv("CMD")
            env_content = os.getenv("ENV_CONTENT", "")
            name=body.get('name')
            user_uid = body.get('user_id')

            # Validate required parameters
            if not all([github_url, docker_user, docker_pass, image_name,name,user_uid]):
                return JsonResponse({
                    "status": "error",
                    "message": "Missing required parameters (githubUrl, dockerUser, dockerPass, imageName, name, user_id)."
                })

            try:
                user = User.objects.get(uid=user_uid)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            

            # Environment variables
            env_vars = {
                "GIT_URL": github_url,
                "DOCKER_USERNAME": docker_user,
                "DOCKER_PASSWORD": docker_pass,
                "IMAGE_NAME": image_name,
                "CMD":cmd,
                "ENV_CONTENT": env_content
            }
            # Docker volume bindings
            repo_name = github_url.split("/")[-1].replace(".git", "")
            

            # Initialize Docker client
            client = docker.from_env()

            # Run the container
            
           # docker run   -e GIT_URL=https://github.com/Sahiiil1406/ServerHealthChecker.git   -e DOCKER_USERNAME=sahil1406   -e DOCKER_PASSWORD=dckr_pat_xtvZyHE9hxT7nYSXW0cPACJlibc   -e IMAGE_NAME=serverhealthchecker   -v /var/run/docker.sock:/var/run/docker.sock   --privileged   final
            # os.system(f"docker run -d -e GIT_URL={github_url} -e DOCKER_USERNAME={docker_user} -e DOCKER_PASSWORD={docker_pass} -e IMAGE_NAME={image_name} -v /var/run/docker.sock:/var/run/docker.sock --privileged final")
            #get logs

            container = client.containers.run(
                    image="final_deploy",  # Replace 'final' with your image name
                    detach=True,
                    environment=env_vars,
                    volumes={
                        "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}
                    },
                    privileged=True
                )

            logs = container.logs(stream=True)
            logs_output = ""
            for log in logs:
               logs_output += log.decode('utf-8')

            # Stop and remove the container and remove image
            
            container.stop()     
            container.remove() 

            #hit a URL to show success:url:http://172.25.96.1:8001/api/webhook ,request type:POST,req.body:{id,image_name,image_port}
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
            
            deployment = Deployments.objects.create(name=name, gitURL=github_url, status='READY', user=user)


            return JsonResponse({
                "status": "success",
                "message": "Container executed successfully.",
                "containerId": container.id,
                "containerLogs": logs_output.strip()
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": "Failed to execute container.",
                "error": str(e),
            })

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method. Use POST."
    })

@login_required
def get_url(request):
    return render(request, 'get_url.html')
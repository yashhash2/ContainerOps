from django.shortcuts import render
import json
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .store import store
from .store import PORT
import os
import docker
# Create your views here.

def update_nginx_config(config_file, base_url, conditions):
    data = [
        "events {",
        "    worker_connections 1024;",
        "}",
        "",
        "http {",
        "   map $subdomain $upstream {"
    ]
    for subdomain, upstream in store.items():
         data.append(f"    {subdomain}   {base_url}:{upstream};")

    # Add the default case
    data.append("    default \"\";")
    data.append("}")
    data.extend([
        "",
        "server {",
        "    listen 8000;",
        f"    server_name ~^(?<subdomain>[^.]+)\\.{base_url};",
        "",
        "    location / {",
        "        if ($upstream = \"\") {",
        "            return 200 \"No such subdomain\";",
        "        }",
        "        proxy_pass $upstream;",
        "    }",
        "}",
        "}",
    ])
    with open(config_file, "w") as file:
        file.write("\n".join(data))

    
@csrf_exempt
def webhook(request):
    global PORT
    if(request.method=='POST'):
        print("Webhook called")
        data = json.loads(request.body)
        print(data)
        #data have id and image_name and image_port
        #create a new container
        client = docker.from_env()
        client.containers.run(data['image_name'],detach=True,ports={data['image_port']:PORT})

        #update the store
        store[data['id']] = PORT
        PORT+=1
        #update the nginx configuration
        update_nginx_config("./test","http://172.25.96.1",store)
        return JsonResponse({"status": "ok"})
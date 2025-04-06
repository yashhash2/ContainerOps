# ContainerOps 🚀

[![Django](https://img.shields.io/badge/Django-3.2-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-20.10-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ContainerOps is a universal Continuous Deployment (CD) tool that simplifies Docker-based application deployment with automated Dockerfile generation and GitHub integration.

## 🌟 Features

- **Automated Dockerfile Generation** - Creates optimized Dockerfiles based on project type
- **GitHub Integration** - OAuth authentication and repository access
- **Real-time Deployment** - Automatically deploys on new commits
- **Container Management** - Full lifecycle control of Docker containers
- **Dashboard** - Monitor containers, view logs

  
## 🛠️ Technologies

- **Backend**: Django (Python)
- **Frontend**: HTML,TailWind CSS
- **Containerization**: Docker, Docker Compose
- **Authentication**: OAuth (GitHub, Google)
- **Database**: PostgreSQL

## 🗄️ Database Schema
![co1](https://github.com/user-attachments/assets/bd21752b-55f5-4778-b95a-3adcde605f28)

## 🏗️ System Architecture
![Screenshot (46)](https://github.com/user-attachments/assets/b7ad8b5b-b13c-4906-ba05-e1838a58c890)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker Engine 20.10+
- GitHub Developer Account (for OAuth)
- PostgreSQL 12+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/containerops.git
   cd containerops
   ```
2. Create and activate virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
   ```
3.Install dependencies:
   ```bash
    cd buildServer
    pip install -r requirements.txt
  ```

4.Set up environment variables (create .env file):
  ```bash
      SECRET_KEY=your_django_secret_key
      DB_NAME=containerops
      DB_USER=postgres
      DB_PASSWORD=postgres
      DB_HOST=localhost
      DB_PORT=5432
      GITHUB_CLIENT_ID=your_github_oauth_id
      GITHUB_CLIENT_SECRET=your_github_oauth_secret
  ```


5.Start development server:
  ```bash
    cd proxy_server
    python manage.py runserver
    cd ../
    cd buildServer
    python manage.py runserver
  ```
  

## 🏁 Conclusion

ContainerOps provides a powerful continuous deployment solution with Docker automation and GitHub integration. With its intuitive interface and automated workflows, teams can focus on development while ensuring reliable deployments.




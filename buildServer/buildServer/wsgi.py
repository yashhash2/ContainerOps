import os
import sys
from django.core.wsgi import get_wsgi_application

# 1. This grabs the path to the OUTER buildServer folder
# __file__ is buildServer/buildServer/wsgi.py
# dirname(__file__) is the inner buildServer folder
# dirname(dirname(__file__)) is the outer buildServer folder where manage.py lives
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Add that outer folder to Python's system path so it can find 'buildServer.settings'
if project_root not in sys.path:
    sys.path.append(project_root)

# 3. Tell Django where the settings are
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buildServer.settings')

application = get_wsgi_application()

# 4. Expose the 'app' variable specifically for Vercel
app = application
import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), ".env")
env = load_dotenv(dotenv_path=dotenv_path, override=True)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_task.settings")

app = Celery("smartnotify")  # Replace 'your_project' with your project's name.

# Configure Celery using settings from Django settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    broker_url=os.getenv("CELERY_BROKER_URL"),
    timezone="Asia/Kathmandu",
)

app.conf.beat_schedule = {
    "fetch-every-five_minutes": {
        "task": "app.hydrology.tasks.fetch_and_index_hydrology_data",
        "schedule": crontab(minute="*/5"),
    },
}

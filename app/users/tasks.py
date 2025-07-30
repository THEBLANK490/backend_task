from celery import shared_task

from app.users.utils import fetch_and_index_hydrology_data


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_and_index_hydrology_data_task():
    """
    A celery beat task to fetch the data from the given url and
    populate it inside the elasticsearch
    """
    fetch_and_index_hydrology_data()

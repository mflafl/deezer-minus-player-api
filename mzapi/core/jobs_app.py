import os
from celery import Celery

celery = Celery('mzapi', broker='redis://127.0.0.1:6379/0',
                result_backend=os.environ['CELERY_DATABASE_URL'])
celery.conf.update(
    imports=['mzapi.jobs'],
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)

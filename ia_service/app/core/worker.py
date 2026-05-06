import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from celery import Celery

celery_app = Celery(
    main="ia_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

import app.core.ia_task
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
celery_app.conf.update(task_track_started=True, result_expires=86400, broker_connection_timeout=5, broker_transport_options={"socket_connect_timeout": 5, "socket_timeout": 5}, redis_socket_connect_timeout=5, redis_socket_timeout=5)

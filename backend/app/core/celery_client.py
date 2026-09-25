from celery import Celery

celery_app = Celery(
    "backend", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_track_started=True,
    result_expires=86400,
    broker_connection_timeout=5,
    broker_transport_options={"socket_connect_timeout": 5, "socket_timeout": 5},
    redis_socket_connect_timeout=5,
    redis_socket_timeout=5,
)

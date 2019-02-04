#cd web
#su -m skiline11 -c "celery worker -A web.celery --concurrency=4 -Q default -n default@%h"
celery worker -A web.celery --concurrency=4 -Q default -n default
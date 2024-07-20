# aliyun_ml_demo

## 正式环境启动
gunicorn django_project_name.wsgi:application --bind 0.0.0.0:8000

## 正式环境启动前检查
python manage.py check --deploy

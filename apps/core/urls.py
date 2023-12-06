from django.urls import path

from apps.core.views import home, celery

urlpatterns = [
    path("", home, name="home"),   # login direciona para home
    path("celery/", celery, name="celery")
]
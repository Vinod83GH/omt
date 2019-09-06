from django.urls import path
from . import views

urlpatterns = [
    path('/data', views.names),
    path('/import', views.import_data),
]
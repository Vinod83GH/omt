from django.urls import path
from . import views

urlpatterns = [
    path('/data', views.names),
    path('/import', views.import_data),
    path('/process_image_ocr',views.process_image_ocr),
    path('/import_stocks',views.process_import_stocks),
]

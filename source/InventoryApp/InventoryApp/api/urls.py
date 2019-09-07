from django.urls import path
from . import views

urlpatterns = [
    path('/data', views.names),
    path('/import', views.import_data),
    path('/process_image_ocr',views.process_image_ocr),
    path('/import_stocks',views.process_import_stocks),
    path('/import_stock_out',views.process_import_stock_out),
    path('/category_expenses',views.get_category_wise_expenses),
    path('/quick_references',views.get_quick_reference_data),
    path('/daily_consumables', views.daily_consumables),
    path('/get_all_data', views.get_all_data),
]

from django.http import JsonResponse
from .tasks import process_input_file,process_ocr_image,process_stock_ins

from InventoryApp.stock.models import StockOut
from InventoryApp.product_catalogue.models import Product, ProductCategory
from django.db.models import Sum
from django.core import serializers
from django.db.models import FloatField, F

def names(request):
    return JsonResponse({'names': ['William', 'Rod', 'Grant']})

def import_data(request):
    # Write your data import logic below
    process_input_file()
    return JsonResponse({'message':'Successfully imported data'})

def process_import_stocks(request):
    process_stock_ins()
    return JsonResponse({'message':'Successfully imported stocks data'})

def process_image_ocr(request):
    process_ocr_image()
    return JsonResponse({'message':'Successfully processed OCR data'})

def get_category_wise_expenses(request):
    # Write your data import logic below
    category_total_cost = list(StockOut.objects.values('product_item__category__desc').annotate(grand_category_total = Sum('total_units')))
    print(category_total_cost)
    # serialized_data = serializers.serialize('json', category_total_cost)
    return JsonResponse(category_total_cost, safe=False) 





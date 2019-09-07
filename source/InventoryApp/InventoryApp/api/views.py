from django.http import JsonResponse
from .tasks import process_input_file,process_ocr_image,process_stock_ins

from InventoryApp.stock.models import *
from InventoryApp.product_catalogue.models import Product, ProductCategory
from django.db.models import Sum
from django.core import serializers
from django.db.models import FloatField, F
from datetime import date

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

def get_quick_reference_data(request):
    response = dict()
    out_of_stock = StockOut.objects.filter(total_units=0)[:4]
    chart_one =list()
    for stock in out_of_stock:
        new_stock = dict()
        new_stock['item_desc'] = stock.product_item.desc
        new_stock['stock'] = stock.total_units
        chart_one.append(new_stock)
    chart_second = list()
    expired_data  = StockOut.objects.filter()[:4]
    for expired in expired_data:
        ex_dict = dict()
        ex_dict['validity'] = 'expired'
        ex_dict['expiry_date']  = '23/08/2019'
        chart_second.append(ex_dict)
    chart_three = []
    min_balances = StockBalance.objects.filter(total_units__lte=5)[:4]
    for min_bal in min_balances:
        min_dict = dict()
        min_dict['item_desc'] = min_bal.product_item.desc
        min_dict['min balance'] = '5'
        min_dict['available'] = min_bal.total_units
        chart_three.append(min_dict)
    product_categories = ProductCategory.objects.all()[:4]
    d0 = date(2008, 9, 1)
    d1 = date(2008, 9, 25)
    delta = d1 - d0
    chart_four = list()
    for cat in product_categories:
        new = dict()
        new['item_desc'] = cat.desc
        new['due_date'] = '25/09/2019'
        new['days_left'] = delta
        chart_four.append(new)
    response['chart_one']=chart_one
    response['chart_second'] = chart_second
    response['chart_three'] = chart_three
    response['chart_four'] = chart_four
    return JsonResponse(response) 





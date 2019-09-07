from django.http import JsonResponse
from .tasks import process_input_file,process_ocr_image,process_stock_ins

from InventoryApp.stock.models import StockOut, StockIn
from InventoryApp.product_catalogue.models import Product, ProductCategory
from django.db.models import Sum
from django.core import serializers
from django.db.models import FloatField, F
from datetime import datetime

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
    select_date = {"date": """strftime('%%m/%%Y', out_date)"""}
    category_total_cost = list(StockOut.objects.extra(select=select_date).values('date').annotate(grand_category_total = Sum('total')))
    
    monthly_expenses_category_wise = list()
    monthly_obj = {}
    # print('Result- {}'.format(category_total_cost))
    for index, item in enumerate(category_total_cost):
        # out_date = {"date": """strftime('%%m/%%Y', entry_date)"""}
        # print('date-item - {} '.format(item))
        out_date = datetime.strptime(item.get('date'), "%m/%Y")
        all_items = list(StockOut.objects.filter(out_date__year=out_date.year, out_date__month=out_date.month).values('product_item__category__desc').annotate(grand_category_total = Sum('total')))
        # print('Date Categories - {}'.format(all_items))
        for category in all_items:
            monthly_obj['date']=item.get('date')
            monthly_obj[category.get('product_item__category__desc')]=category.get('grand_category_total')
        
        monthly_expenses_category_wise.append(monthly_obj)
        
    return JsonResponse(monthly_expenses_category_wise, safe=False) 





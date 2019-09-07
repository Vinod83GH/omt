from django.http import JsonResponse
from .tasks import process_input_file,process_ocr_image,process_stock_ins, process_stock_out_data

from InventoryApp.stock.models import *
from InventoryApp.product_catalogue.models import Product, ProductCategory
from django.db.models import Sum
from django.core import serializers
from django.db.models import FloatField, F
from datetime import date
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

def process_import_stock_out(request):
    process_stock_out_data()
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
        monthly_obj = {}
        for category in all_items:
            monthly_obj['date']=item.get('date')
            monthly_obj[category.get('product_item__category__desc')]=category.get('grand_category_total')

        monthly_expenses_category_wise.append(monthly_obj)

    return monthly_expenses_category_wise

def daily_consumables(request):
    current_month = datetime.now().month
    current_year = datetime.now().year

    stocks = StockOut.objects.filter(
        out_date__year=current_year,
        out_date__month=current_month
    )

    count = 0
    # while stocks.count() == 0:

    #     stocks = StockOut.objects.filter(
    #         out_date__year=current_year,
    #         out_date__month=current_month
    #     )

    #     if count > 10:
    #         break

    #     count += 1

    #     current_month = current_month-1

    #     if current_month == 0:
    #         current_month = 12
    #         current_year = current_year-1

    # stocks_total = stocks.values_list('total', flat=True)

    data = []
    # for total in stocks_total:
    #     data.append(float(total))


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


    return data

def get_all_data(request):
    return_data = {
        'daily_consumables': daily_consumables(request),
        'category_expenses': get_category_wise_expenses(request)
    }

    return JsonResponse(return_data, safe=False)

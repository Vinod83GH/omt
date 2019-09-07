import os
import csv
import time
import json
from datetime import datetime

from InventoryApp.product_catalogue.models import  *
from .AbbyyOnlineSdk import *
from .process_table_data import process_table_data
from InventoryApp.stock.models import StockIn
processor = None

def process_stock_ins():
    dir_path = './InventoryApp/stock_inputs/'
    if os.path.isdir(dir_path):
        files_in_dir = os.listdir(dir_path)
    if files_in_dir:
        for input_file in files_in_dir:
            if input_file.endswith('.csv'):
                path = '{}{}'.format(dir_path,input_file)
                with open(path, encoding="utf-8-sig") as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    line_count = 0
                    for row in csv_reader:
                        product = None
                        row = dict(row)
                        print('each row: ',row)
                        if line_count == 0:
                            print("header: ", row)
                            line_count +=1
                        else:
                            product = None
                            product_unit = None
                            if row:
                                stock_in = StockIn()
                                product_code = row.get('Product Code')
                                cost_per_unit  = 0 if not row.get('COST/UNIT') else float(row.get('COST/UNIT'))
                                opening_bal = 0 if not row.get('OPG. BAL') else int(row.get('OPG. BAL'))
                                stock_received = 0 if not row.get('Stock Receipt') else int(row.get('Stock Receipt'))
                                total_units = opening_bal + stock_received
                                try:
                                    product = Product.objects.get(code=product_code)
                                    code = ''
                                    if row.get('UOM'):
                                        code = row.get('UOM')
                                    print('Product UOM - {}'.format(code))
                                    product_unit = ProductUnit.objects.get(code = code)

                                    print('Product details - {}; {}'.format(row.get('OPG. BAL'), row.get('COST/UNIT')))
                                    
                                    stock_in.product_item = product
                                    stock_in.unit = product_unit
                                    stock_in.cost_per_unit = cost_per_unit
                                    stock_in.total_units = total_units
                                    stock_in.total = stock_in.total_cost
                                    stock_in.tax = 0
                                    stock_in.entry_date = '2019-01-01'
                                    # stock_in.save()
                                    print('Product saved - {}'.format(product_code))
                                
                                except Exception as e:
                                    print('Product save ERROR - {}; error - {}'.format(product_code, e))
                                



def process_input_file():
    dir_path = './InventoryApp/all_product_inputs/'
    files_in_dir = []
    if os.path.isdir(dir_path):
        files_in_dir = os.listdir(dir_path)
    if files_in_dir:
        for input_file in files_in_dir:
            if input_file.endswith('.csv'):
                path = '{}{}'.format(dir_path,input_file)
                with open(path, encoding="utf-8-sig") as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    line_count = 0
                    for row in csv_reader:
                        product = None
                        row = dict(row)
                        print('each row: ',row)
                        if line_count == 0:
                            print(f'Column names are {", ".join(row)}')
                            line_count += 1
                        else:
                            if row.get('SL. NO.') !='':
                                prod_code = row.get('Product Code','')
                                print(prod_code)
                                product = None
                                product_cat = None
                                product_unit = None
                                try:
                                    product = Product.objects.get(code = prod_code)
                                except:
                                    product = None
                                if product is None:
                                    product = Product()
                                if row.get('Category'):
                                    cat = row.get('Category')
                                    if cat == 'Pantry':
                                        product_cat = ProductCategory.objects.get(code='PANTRY-CONSUMES')
                                    if cat == 'Toiletries':
                                        product_cat = ProductCategory.objects.get(code='TOILETRIES')
                                    if cat == 'Cleaning Consumables':
                                        product_cat = ProductCategory.objects.get(code='CLEANING-CONSUMES')
                                    if cat == 'Stationaries':
                                        product_cat = ProductCategory.objects.get(code='STATIONARY')
                                if row.get('UOM'):
                                    code = row.get('UOM')
                                    try:
                                        product_unit = ProductUnit.objects.get(code = code)
                                    except:
                                        product_unit = None
                                        print('Product failed to add -  {}'.format(prod_code))

                                product.code = prod_code
                                product.desc = row.get('ITEMS','')
                                if product_cat is not None:
                                    product.category = product_cat
                                if product_unit is not None:
                                    product.default_unit = product_unit
                                product.default_cost = 0
                                product.save()
                            line_count += 1
                    print(f'Processed {line_count} lines.')

def process_ocr_image():
    print("Inside the procdess OCR Image")
    global processor
    processor = AbbyyOnlineSdk()
    setup_processor()
    language = 'English'
    output_format = 'txt'
    dir_path = './InventoryApp/ocr_inputs/'
    output_dir_path = './InventoryApp/ocr_outputs/'
    files_in_dir = []

    if os.path.isdir(dir_path):
        files_in_dir = os.listdir(dir_path)
        print("files in dir: ",files_in_dir)
    if files_in_dir:
        count = 0
        for input_file in files_in_dir:
            target_file=''
            target_file = '{}{}{}'.format('result',count,'.txt') 
            source_file = '{}{}'.format(dir_path,input_file)
            target_file = '{}{}'.format(output_dir_path,target_file)
            if os.path.isfile(source_file):
                recognize_file(source_file, target_file, language, output_format)
            else:
                print("No such file: {}".format(source_file))

def setup_processor():
    if "ABBYY_APPID" in os.environ:
        processor.ApplicationId = os.environ["ABBYY_APPID"]

    if "ABBYY_PWD" in os.environ:
        processor.Password = os.environ["ABBYY_PWD"]

    # Proxy settings
    if "http_proxy" in os.environ:
        proxy_string = os.environ["http_proxy"]
        print("Using http proxy at {}".format(proxy_string))
        processor.Proxies["http"] = proxy_string

    if "https_proxy" in os.environ:
        proxy_string = os.environ["https_proxy"]
        print("Using https proxy at {}".format(proxy_string))
        processor.Proxies["https"] = proxy_string

def recognize_file(file_path, result_file_path, language, output_format):
    print("Uploading..")
    settings = ProcessingSettings()
    settings.Language = language
    settings.OutputFormat = output_format
    task = processor.process_image(file_path, settings)
    if task is None:
        print("Error")
        return
    if task.Status == "NotEnoughCredits":
        print("Not enough credits to process the document. Please add more pages to your application's account.")
        return

    print("Id = {}".format(task.Id))
    print("Status = {}".format(task.Status))

    # Wait for the task to be completed
    print("Waiting..")
    while task.is_active():
        time.sleep(5)
        print(".")
        task = processor.get_task_status(task)
    print("Status = {}".format(task.Status))

    if task.Status == "Completed":
        if task.DownloadUrl is not None:
            processor.download_result(task, result_file_path)
            print("Result was written to {}".format(result_file_path))
            process_table_data(result_file_path)
    else:
        print("Error processing task")





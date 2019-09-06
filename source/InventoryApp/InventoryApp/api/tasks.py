import os
import csv
from InventoryApp.product_catalogue.models import  *


def process_input_file():
    dir_path = './InventoryApp/all_product_inputs/'
    files_in_dir = []
    if os.path.isdir(dir_path):
        files_in_dir = os.listdir('./InventoryApp/all_product_inputs/')
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
                                if row.get('UOM'):
                                    code = row.get('UOM')
                                    try:
                                        product_unit = ProductUnit.objects.get(code = code)
                                    except:
                                        product_unit = None
                                print("product: ",product)
                                print("product_cat: ",product_cat)
                                print("product_unit: ",product_unit)

                                product.code = prod_code
                                product.desc = row.get('ITEMS','')
                                if product_cat is not None:
                                    product.category = product_cat
                                if product_unit is not None:
                                    product.default_unit = product_unit
                                product.default_cost = 0
                                product.save()
                            line_count += 1
                    # print(f'Processed {line_count} lines.')


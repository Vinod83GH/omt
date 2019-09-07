# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views import View

from django.shortcuts import render

from InventoryApp.product_catalogue.models import Product, ProductUnit
from InventoryApp.stock.models import StockOut, StockIn, StockBalance

# Create your views here.
from django.http import JsonResponse

class ProductFormView(View):

    template_name = "product_form.html"
    error_template_name = "error.html"

    def get(self, request, product_code, **kwargs):
        try:
            stockbal = StockBalance.objects.filter(
                product_item__code=product_code
            )

            if not stockbal:
                return render(request, self.error_template_name, {
                    'fail_message': 'Stock Balance Record Not Found'
                })

            info = self.get_stock_info()

            return render(request, self.template_name, {
                'stockbal': stockbal[0],
                'stocks': stockbal,
                'info': info
            })
        except Exception as e:
            pass

    def post(self, request, product_code, **kwargs):
        no_of_items = request.POST.get('no_of_items')
        stock_in_out = request.POST.get('stock_in_out')
        cost_per_unit = request.POST.get('cost_per_unit', '')

        if stock_in_out == 'stock_out':
            cost_per_unit = request.POST.get('cost_per_unit_select', '')

        stocks = StockBalance.objects.filter(
            product_item__code=product_code
        )

        if int(no_of_items) <= 0:
            return render(
                request,
                self.template_name,
                {
                    'stockbal': stocks[0],
                    'fail_message': 'No. of items should be greater than 0'
                }
            )

        info = self.get_stock_info()

        if stock_in_out == 'stock_in':
            self.stock_in(
                request,
                stocks[0],
                product_code,
                no_of_items
            )
        else:
            self.stock_out(
                request,
                stocks[0],
                product_code,
                no_of_items
            )

        return render(
            request,
            self.template_name,
            {
                'stockbal': stocks[0],
                'stocks': stocks,
                'message': 'Product Updated Successfully',
                'info': info
            }
        )

    def get_stock_info(self):
        data = {}
        data['units'] = ProductUnit.objects.all()

        return data

    def stock_out(self, request, stockbal, product_code, no_of_items):
        unit = request.POST.get('unit', '')
        cost_per_unit = request.POST.get('cost_per_unit_select', '')

        unit = ProductUnit.objects.get(code=unit)

        StockOut.objects.create(
            product_item=stockbal.product_item,
            unit=unit,
            cost_per_unit=cost_per_unit,
            total_units=int(no_of_items),
            total=float(cost_per_unit) * float(no_of_items)
        )

    def stock_in(self, request, stockbal, product_code, no_of_items):
        unit = request.POST.get('unit', '')
        cost_per_unit = request.POST.get('cost_per_unit', '')
        tax = request.POST.get('tax', '')
        expiry_days = request.POST.get('expiry_days', '')
        manufacturing_date = request.POST.get('manufacturing_date', '')

        unit = ProductUnit.objects.get(code=unit)

        StockIn.objects.create(
            product_item=stockbal.product_item,
            unit=unit,
            cost_per_unit=cost_per_unit,
            tax=tax,
            total_units=int(no_of_items),
            expiry_days=expiry_days,
            manufacturing_date=manufacturing_date + ' 00:00:00',
            total=float(cost_per_unit) * float(no_of_items)
        )

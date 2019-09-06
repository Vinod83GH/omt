# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from InventoryApp.product_catalogue.models import Product, ProductCategory
from .models import StockIn, StockOut, StockBalance

# Register your models here.
class StockInAdmin(admin.ModelAdmin):
    
    raw_id_fields = ('product_item',)
    
    readonly_fields = ('total_cost', )
    
    list_display = (
        'product_item',
        'cost_per_unit',
        'total_units',
        # 'get_unit_desc',
        'tax',
        'total_cost'
    )

    list_filter = [
        'product_item__category__desc'
    ]

    search_fields = ['product_item__code','product_item__desc', 'product_item__category__desc']

    # def get_product_desc(self, obj):
    #     return obj.product_item.desc

    # def get_unit_desc(self, obj):
    #     return obj.unit.desc

    # get_product_desc.short_description = 'Product'
    # get_product_desc.boolean = True
    
    # get_unit_desc.short_description = 'Unit'
    # get_unit_desc.boolean = True

    class Meta:
        model = StockIn
        verbose_name = 'Stock Entry'
        verbose_name_plural = 'Stock Entry'


class StockOutAdmin(admin.ModelAdmin):
    list_display = (
        'get_product_desc',
        'cost',
        'get_unit_desc',
        'tax',
        'total'
    )

    list_filter = [
        'product_item__category__desc'
    ]

    search_fields = ['product_item__code','product_item__desc', 'product_item__category__desc']

    def get_product_desc(self, obj):
        return obj.product_item.desc

    def get_unit_desc(self, obj):
        return obj.unit.desc

    get_product_desc.short_description = 'Product'
    get_product_desc.boolean = True

    class Meta:
        model = StockOut
        verbose_name = 'Stock out'
        verbose_name_plural = 'Stock out'


admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
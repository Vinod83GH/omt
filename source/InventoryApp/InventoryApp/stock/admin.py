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
        'get_category',  
        'cost_per_unit',
        'unit',
        'total_units',
        'tax',
        'total_cost',
        'entry_date'
    )

    list_filter = [
        'product_item__category__desc'
    ]

    search_fields = ['product_item__code','product_item__desc', 'product_item__category__desc']

    def get_category(self, obj):
        if not obj.product_item.category:
            return ''
        
        return str(obj.product_item.category)

    class Meta:
        model = StockIn
        verbose_name = 'Stock Entry'
        verbose_name_plural = 'Stock Entry'


class StockOutAdmin(admin.ModelAdmin):
    raw_id_fields = ('product_item',)
    
    list_display = (
        'product_item',
        'get_category',        
        'unit',
        'cost_per_unit',
        'total_units',
        'total_cost',
        'out_date'
    )

    list_filter = [
        'product_item__category__desc'
    ]

    search_fields = ['product_item__code','product_item__desc', 'product_item__category__desc']
    
    def get_category(self, obj):
        if not obj.product_item.category:
            return ''
        
        return str(obj.product_item.category)

    class Meta:
        model = StockOut
        verbose_name = 'Stock out'
        verbose_name_plural = 'Stock out'
        

class StockBalanceAdmin(admin.ModelAdmin):
    list_display = (
        'product_item',
        'unit',
        'cost_per_unit',
        'total_units',
        'total_cost'
    )

    list_filter = [
        'product_item__category__desc'
    ]

    search_fields = ['product_item__code','product_item__desc', 'product_item__category__desc']

    class Meta:
        model = StockBalance
        verbose_name = 'StockBalance'
        verbose_name_plural = 'StockBalance'


admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
admin.site.register(StockBalance, StockBalanceAdmin)
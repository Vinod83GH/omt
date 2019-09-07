# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from InventoryApp.product_catalogue.models import Product, ProductCategory, ProductSubCategory, ProductUnit

# Register your models here.
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'desc'
    )

    search_fields = ['code','desc']

    # def get_product_desc(self, obj):
    #     return obj.product.desc

    # def get_unit_desc(self, obj):
    #     return obj.unit.desc

    # get_product_desc.short_description = 'Product'
    # get_product_desc.boolean = True

    class Meta:
        model = ProductCategory
        verbose_name = 'ProductCategory'
        verbose_name_plural = 'ProductCategories'


class ProductSubCategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('category', )

    list_display = (
        'category',
        'code',
        'desc'
    )

    search_fields = ['code','desc', 'category__desc']

    class Meta:
        model = ProductSubCategory
        verbose_name = 'ProductSubCategory'
        verbose_name_plural = 'ProductSubCategories'

class ProductUnitAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'desc'
    )

    search_fields = ['code','desc']

    # def get_product_desc(self, obj):
    #     return obj.product.desc

    # def get_unit_desc(self, obj):
    #     return obj.unit.desc

    # get_product_desc.short_description = 'Product'
    # get_product_desc.boolean = True

    class Meta:
        model = ProductUnit
        verbose_name = 'ProductUnit'
        verbose_name_plural = 'ProductUnits'

class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category', )

    list_display = (
        'code',
        'desc',
        'brand',
        'category',
        'default_unit',
        'default_cost',
        'minimum_balance',
        'qr_code_image'
    )

    list_filter = [
        'category__desc'
    ]

    search_fields = ['code','desc', 'category__desc', 'brand']

    def qr_code_image(self, obj):
        return format_html('<img src="{}.png" width="150" style="cursor: pointer;" onclick="newWindow = window.open(\'{}.png\');" /><p><a href="javascript:void(0);" onclick="newWindow = window.open(\'{}.png\'); newWindow.print();">Print</a></p>'.format(
            settings.MEDIA_URL + 'QR_CODES/' + str(obj.id),
            settings.MEDIA_URL + 'QR_CODES/' + str(obj.id),
            settings.MEDIA_URL + 'QR_CODES/' + str(obj.id)
        ))

    qr_code_image.allow_tags = True
    qr_code_image.short_description = 'Column description'


    class Meta:
        model = Product
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


admin.site.register(ProductUnit, ProductUnitAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductSubCategory, ProductSubCategoryAdmin)
admin.site.register(Product, ProductAdmin)

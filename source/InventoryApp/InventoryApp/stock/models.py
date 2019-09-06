'''UserNotification related models'''
from django.db import models
from django.conf import settings
from InventoryApp.product_catalogue.models import Product, ProductUnit

class StockIn(models.Model):
    '''Stock entry'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=4, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateTimeField(null=True)
    expiry_days = models.IntegerField(default=0)

class StockOut(models.Model):
    '''Stock consumption'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=4, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class StockBalance(models.Model):
    '''Stock consumption'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=4, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)


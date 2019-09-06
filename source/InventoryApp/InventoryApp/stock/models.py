'''UserNotification related models'''
from django.db import models
from django.conf import settings
from InventoryApp.product_catalogue.models import Product, ProductUnit
from datetime import datetime

class StockIn(models.Model):
    '''Stock entry'''
    product_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_units = models.IntegerField(default=0)
    tax = models.DecimalField(max_digits=4, decimal_places=2)
    manufacturing_date = models.DateTimeField(null=True, blank=True)
    expiry_days = models.IntegerField(default=0)
    entry_date = models.DateTimeField(null=False, editable=False, default=datetime.now)
    
    @property
    def total_cost(self):
        if not self.cost_per_unit:
            return 0
        
        return '{}'.format(self.cost_per_unit * self.total_units)

class StockOut(models.Model):
    '''Stock consumption'''
    product_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_units = models.IntegerField(default=0)
    out_date = models.DateTimeField(null=False, default=datetime.now, editable=False)
    
    @property
    def total_cost(self):
        if not self.cost_per_unit or not self.total_units:
            return 0
        
        return '{}'.format(self.cost_per_unit * self.total_units)

class StockBalance(models.Model):
    '''Stock balance'''
    product_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_units = models.IntegerField(default=0)
    
    @property
    def total_cost(self):
        if not self.cost_per_unit or not self.total_units:
            return 0
        
        return '{}'.format(self.cost_per_unit * self.total_units)


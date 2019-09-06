'''UserNotification related models'''
from django.db import models
from django.conf import settings
from InventoryApp.product_catalogue.models import Product, ProductUnit
from datetime import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Q

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


@receiver(post_save, sender=StockIn)
def update_stock_balance_from_entry(sender, instance, created, **kwargs):
    """Signal handler to save the user follows object."""

    print(
        'Stock-In: CREATED'
    )
    balance = None
    try:
        balance = StockBalance.objects.get(product_item=instance.product_item, unit=instance.unit, cost_per_unit=instance.cost_per_unit)
    except Exception as e:
        StockBalance.objects.create(product_item=instance.product_item, unit=instance.unit, cost_per_unit=instance.cost_per_unit, total_units=instance.total_units)
        return

    try:
        balance.total_units += instance.total_units
        balance.save()
        
        print('Stock balance updated on stock in for - {}'.format(instance.id))
    except Exception as e:
        print(
            'Error saving stock balance while stocking in : {}'.format(e)
        )
        

@receiver(post_save, sender=StockOut)
def update_stock_balance(sender, instance, created, **kwargs):
    """Signal handler to save the user follows object."""

    print(
        'Stock-Out: CREATED/updated'
    )
    balance = None
    query = Q(product_item=instance.product_item) & Q(unit=instance.unit) & Q(cost_per_unit=instance.cost_per_unit)
    try:
        balance = StockBalance.objects.get(query)
    except Exception as e:
        stock_in = StockIn.objects.get(query)
        total_balance_units = stock_in.total_units - instance.total_units
        StockBalance.objects.create(product_item=instance.product_item, unit=instance.unit, cost_per_unit=instance.cost_per_unit, total_units=total_balance_units)
        return

    try:
        balance.total_units -= instance.total_units
        balance.save()
        
        print('Stock balance updated for - {}'.format(instance.id))
    except Exception as e:
        print(
            'Error saving stock balance record: {}'.format(e)
        )



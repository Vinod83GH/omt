'''UserNotification related models'''
import os
from django.db import models
from django.conf import settings
# from InventoryApp.stock.models import StockOut

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class ProductCategory(models.Model):
    '''Product category'''
    code = models.CharField(max_length=50, null=False, unique=True)
    desc = models.CharField(max_length=500, null=True)

    # @property
    # def total_cost(self):
    #     StockOut.objects.
    #     if not self.cost_per_unit:
    #         return 0

    #     return '{}'.format(self.cost_per_unit * self.total_units)

    def __str__(self):
        return '{}'.format(self.desc)

class ProductSubCategory(models.Model):
    '''Product sub-category'''
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, null=False, unique=True)
    desc = models.CharField(max_length=500, null=True)

class ProductUnit(models.Model):
    '''Product units'''
    code = models.CharField(max_length=10, null=False, unique=True)
    desc = models.CharField(max_length=500, null=True)

    def __str__(self):
        return '{}'.format(self.desc)

# Create your models here.
class Product(models.Model):
    '''Product model'''
    code = models.CharField(max_length=50, unique=True, null=False)
    desc = models.CharField(max_length=1000, null=False)
    brand = models.CharField(max_length=1000, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    default_unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    default_cost = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_balance = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.desc)

@receiver(post_save, sender=Product)
def generate_qr_code(sender, instance, **kwargs):
    import pyqrcode

    path = settings.MEDIA_ROOT + '/QR_CODES/'

    if not os.path.exists(path):
        os.makedirs(path)

    url = pyqrcode.create('http://192.168.3.136:8000/product_catalogue/' + instance.code)
    url.png(path + str(instance.id) + '.png', scale=8)

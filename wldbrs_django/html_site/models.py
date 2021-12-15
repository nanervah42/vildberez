from django.db import models

# Create your models here.
class MainBase(models.Model):
    item_id = models.IntegerField(unique=True, blank=None)
    brand_name = models.CharField(max_length=250)
    goods_name = models.CharField(max_length=250)
    img = models.CharField(max_length=250)
    price_now = models.IntegerField(blank=None)
    price_min = models.IntegerField(blank=None)
    price_max = models.IntegerField(blank=None)
    timer = models.BigIntegerField(default=0)
    b_count = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    flag = models.BooleanField()
    company_name = models.CharField(max_length=100)
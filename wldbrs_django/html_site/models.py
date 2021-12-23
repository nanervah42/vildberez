from django.db import models


class wb_base(models.Model):
    item_id = models.BigIntegerField(primary_key=True, unique=True, blank=None)
    brand_name = models.CharField(max_length=250)
    goods_name = models.CharField(max_length=250)
    img = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    price_now = models.IntegerField(blank=None)
    price_prev = models.IntegerField(blank=None)
    price_min = models.IntegerField(blank=None)
    price_max = models.IntegerField(blank=None)
    b_count = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    company_name = models.CharField(max_length=50)
    product_type = models.CharField(max_length=50)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_time']
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class pizza(models.Model):
    sno = models.IntegerField(primary_key=True)
    pizza_name = models.CharField(max_length=100)
    pizza_desc = models.CharField(max_length=250)
    pizza_price= models.IntegerField()
    image = models.ImageField(upload_to="pizza_images")


class Cart(models.Model):
    
    sno = models.ForeignKey(pizza, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    sno = models.ForeignKey(pizza, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)

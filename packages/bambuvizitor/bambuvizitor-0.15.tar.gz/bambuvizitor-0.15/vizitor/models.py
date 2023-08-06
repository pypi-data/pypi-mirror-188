from django.db import models
from django.contrib.auth.models import User

from informasaun.models import  *

# Create your models here.

class Order(models.Model):
    status_hare = models.BooleanField(default=False,verbose_name='Staus hare')
    status_resposta = models.BooleanField(default=False,verbose_name='Staus resposta')  
    resposta = models.TextField(verbose_name='resposta',null=True, blank=True)  
    data_order = models.DateField(null=True, blank=True)
    user_order = models.ForeignKey(User, on_delete = models.CASCADE,null=True, blank=True)
    deskrisaun = models.TextField(null=True, blank=True)
    def save(self):
        super().save()
    def __str__(self):
        return "{}. {}".format(self.status_hare, self.status_resposta)





class ListaOrder(models.Model):
    total_order			= models.CharField(max_length=150)
    presu_ida			= models.CharField(max_length=150)
    presu_order			= models.CharField(max_length=150)
    # status_hare = models.BooleanField(default=False,verbose_name='Staus hare')
    # status_resposta = models.BooleanField(default=False,verbose_name='Staus resposta')  
    # data_order = models.DateField(null=True, blank=True)
    produtu = models.ForeignKey(Produtu, on_delete = models.CASCADE,null=True, blank=True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE,null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    hashed = models.TextField(null=True, blank=True)
    def save(self):
        super().save()
    def __str__(self):
        return "{}. {}".format(self.total_order, self.presu_ida)

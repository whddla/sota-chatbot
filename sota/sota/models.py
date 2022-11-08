from django.db import models
from django.conf import settings
from django.utils import timezone

class user(models.Model):
    idx = models.IntegerField(null=False,primary_key =True),
    name = models.CharField(max_length=30, null=False),
    id = models.CharField(max_length=30, null=False),
    pw = models.CharField(max_length=30, null=False),
    p_pw = models.IntegerField(max_length=6, null=False)

class transation(models.Model):
    idx = models.IntegerField(null=False,primary_key =True),
    a_kind = models.IntegerField(null=False),
    i_kind = models.IntegerField(null=False),
    account = models.CharField(max_length=30, null=False),
    amount = models.CharField(max_length=30, null=False),
    remain = models.IntegerField(default = 0, null=False),
    date = models.DateField(null=False),
    user_idx = models.ForeignKey(user,on_delete=models.CASCADE, null=False)

class card(models.Model):
    idx = models.IntegerField(null=False,primary_key =True),
    card_num = models.CharField(max_length=20),
    account = models.CharField(max_length=20),
    card_pw = models.IntegerField(max_length=4, null=False),
    loss = models.IntegerField(default = 0, null=False),
    user_idx = models.ForeignKey(user,on_delete=models.CASCADE, blank=True, null=True),

class d_product(models.Model):
    idx = models.IntegerField(null=False, primary_key=True),
    name = models.CharField(null=False, max_length=30),
    limit = models.CharField(null=False, max_length=30),
    rate = models.CharField(null=False, max_length=30),
    kind = models.CharField(null=False, max_length=30),
    time = models.CharField(null=False, max_length=30),

class l_product(models.Model):
    idx = models.IntegerField(null=False, primary_key=True),
    name = models.CharField(null=False, max_length=30),
    limit = models.CharField(null=False, max_length=30),
    rate = models.CharField(null=False, max_length=30),
    kind = models.CharField(null=False, max_length=30),
    time = models.CharField(null=False, max_length=30),

class c_product(models.Model):
    idx = models.IntegerField(null=False, primary_key=True),
    name = models.CharField(null=False, max_length=30),
    card_idx = models.ForeignKey(card,on_delete=models.CASCADE, null=False)
    benefit = models.IntegerField()

class deposit(models.Model):
    idx = models.IntegerField(null=False, primary_key=True),
    deposit_num = models.CharField(null=False, max_length=30),
    d_product_idx = models.ForeignKey(d_product,on_delete=models.CASCADE,null=False),
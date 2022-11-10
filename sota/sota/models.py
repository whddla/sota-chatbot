from django.db import models

class CProduct(models.Model):
    idx = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    benefit = models.IntegerField()
    card_idx = models.ForeignKey('Card', models.DO_NOTHING, db_column='card_idx', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'c_product'


class Card(models.Model):
    idx = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='user_idx')
    card_num = models.CharField(max_length=30)
    account = models.CharField(max_length=30)
    card_pw = models.IntegerField()
    loss = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    remain = models.IntegerField(blank=True, null=True)
    last_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'card'


class DProduct(models.Model):
    idx = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    limited = models.CharField(max_length=30)
    time = models.CharField(max_length=10)
    rate = models.CharField(max_length=10)
    kind = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'd_product'


class Deposit(models.Model):
    idx = models.AutoField(primary_key=True)
    deposit_num = models.CharField(max_length=30)
    d_product_idx = models.ForeignKey(DProduct, models.DO_NOTHING, db_column='d_product_idx')
    user_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='user_idx', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    remain = models.IntegerField(blank=True, null=True)
    limit_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deposit'


class LProduct(models.Model):
    idx = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    limited = models.CharField(max_length=30)
    time = models.CharField(max_length=10)
    rate = models.CharField(max_length=10)
    kind = models.CharField(max_length=20)
    user_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='user_idx', blank=True, null=True)
    account = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    remain = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'l_product'


class Transation(models.Model):
    idx = models.AutoField(primary_key=True)
    kind = models.IntegerField()
    account = models.CharField(max_length=50)
    amount = models.CharField(max_length=30)
    remain = models.IntegerField(blank=True, null=True)
    details = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    user_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='user_idx')

    class Meta:
        managed = False
        db_table = 'transation'


class User(models.Model):
    idx = models.AutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=50)
    pw = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    addr = models.CharField(max_length=50)
    p_pw = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'
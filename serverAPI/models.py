from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.


class CheckPoint(models.Model):
    owner = models.CharField(max_length=255)
    round = models.PositiveIntegerField()
    data_hash = models.CharField(max_length=255)
    result = models.PositiveIntegerField()

    class Meta:
        db_table = 'checkpoint'
        unique_together = ("owner", "round")


class ShortTermCache(models.Model):
    owner = models.CharField(max_length=255, default="")
    create_round = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    loc_x = models.FloatField()
    loc_y = models.FloatField()
    type = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(3)
    ])
    content = models.CharField(max_length=256)
    acc_count = models.IntegerField(default=0)
    uploaded = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'short_term_cache'
        unique_together = ("owner","create_time", "loc_x", "loc_y", "type")


class LongTermCache(models.Model):
    owner = models.CharField(max_length=255, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    create_round = models.IntegerField(default=0)
    upload_round = models.PositiveIntegerField()
    loc_x = models.FloatField()
    loc_y = models.FloatField()
    type = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(3)
    ])
    content = models.CharField(max_length=256)
    data_hash = models.CharField(max_length=255, default="")

    class Meta:
        db_table = 'long_term_cache'
        unique_together = ("owner","create_time", "loc_x", "loc_y", "type")


class SelfInfo(models.Model):
    reg_time = models.DateTimeField()
    address = models.CharField(max_length=255, primary_key=True)
    private_key = models.CharField(max_length=255)
    loc_x = models.IntegerField()
    loc_y = models.IntegerField()
    chain_id = models.CharField(max_length=255)

    current_round = models.PositiveIntegerField()
    round_time = models.DateTimeField(default=timezone.now())
    bc_port = models.CharField(max_length=5)
    last_updated = models.DateTimeField(default=timezone.now())

    node_status = models.IntegerField(default=0)
    data_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'self_info'


class AdjInfo(models.Model):
    nodeIP = models.CharField(max_length=255, default="")
    selfAddr = models.CharField(max_length=255, default="")
    destAddr = models.CharField(max_length=255, default="")

    class Meta:
        db_table = 'adj_info'


class dataPoint(models.Model):
    loc_x = models.FloatField()
    loc_y = models.FloatField()
    type = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(3)
    ])
    content = models.CharField(max_length=256)
    popularity = models.IntegerField()

    class Meta:
        db_table = 'map_data'
        unique_together = ("loc_x", "loc_y", "type")


class data(models.Model):
    create_time = models.DateTimeField()
    upload_time = models.DateTimeField(auto_now_add=True)
    create_round = models.IntegerField(default=0)
    upload_round = models.PositiveIntegerField()
    loc_x = models.FloatField()
    loc_y = models.FloatField()
    type = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(3)
    ])
    data_hash = models.CharField(max_length=256)
    content = models.CharField(max_length=256)
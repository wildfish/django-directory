from django.db import models


class TestModel(models.Model):
    field_a = models.BooleanField()


class TestModelB(models.Model):
    field_b = models.BooleanField()


class MultipleFieldModel(models.Model):
    first = models.IntegerField(verbose_name='first field')
    second = models.IntegerField()
    third = models.IntegerField()

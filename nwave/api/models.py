from django.db import models


class Asset(models.Model):
    asset = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.asset


class Column(models.Model):
    column = models.CharField(max_length=250)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='column')

    def __str__(self):
        return self.column

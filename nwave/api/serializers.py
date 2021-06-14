from rest_framework import serializers
from .models import Asset, Column


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ('id', 'Asset')


class ColumnSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Column
        fields = (
            'id',
            'column',
            'value',
            'asset',
            'timestamp'
        )

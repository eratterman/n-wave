from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from .models import Asset, Column


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'asset']


class ColumnSerializer(serializers.ModelSerializer):
    column = serializers.StringRelatedField(many=True)

    class Meta:
        model = Asset
        fields = ['id', 'asset', 'column']


# class ParquetSerializer(serializers.Serializer):
#     asset = serializers.CharField(max_length=50)


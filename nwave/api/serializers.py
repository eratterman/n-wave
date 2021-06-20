from rest_framework import serializers
from .models import Asset, Column


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'asset']


class ColumnSerializer(serializers.ModelSerializer):
    column = serializers.StringRelatedField(many=False)

    class Meta:
        model = Asset
        fields = ['id', 'asset', 'column']

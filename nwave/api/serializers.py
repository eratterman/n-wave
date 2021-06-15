# from rest_framework import serializers
# from .models import Asset, Column
#
#
# class AssetSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Asset
#         fields = ('id', 'asset')
#
#
# class ColumnSerializer(serializers.HyperlinkedModelSerializer):
#     columns = serializers.StringRelatedField(many=True)
#
#     class Meta:
#         model = Asset
#         fields = (
#             'asset',
#             'columns'
#         )

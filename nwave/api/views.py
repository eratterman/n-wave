from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AssetSerializer, ColumnSerializer
from .models import Asset, Column


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all().order_by('asset')
    serializer_class = AssetSerializer

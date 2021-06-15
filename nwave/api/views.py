from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
# from .serializers import AssetSerializer, ColumnSerializer
# from .models import Asset, Column
from .forms import FileFieldForm


# class ImportFilesView(FormView):
#     form_class = FileFieldForm
#     template_name = 'import.html'
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 print(f)
#
#             # return self.form_valid(form)
#             return render(request, self.template_name, {'form': None})
#
#         return render(request, self.template_name, {'form': form})
#         # else:
#         #     return self.form_invalid(form)


# class AssetViewSet(viewsets.ModelViewSet):
#     queryset = Asset.objects.all().order_by('asset')
#     serializer_class = AssetSerializer
#
#
# class ColumnViewSet(viewsets.ModelViewSet):
#     queryset = Column.objects.all().order_by('column')
#     serializer_class = ColumnSerializer

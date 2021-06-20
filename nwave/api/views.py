from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .serializers import AssetSerializer, ColumnSerializer
from .models import Asset, Column
from .forms import FileFieldForm
from django.conf import settings as conf_settings
from . import utils
import json


class ImportFilesView(FormView):
    form_class = FileFieldForm
    template_name = 'import.html'
    pq_path = conf_settings.PARQUET_FILES_DIR / 'nwave.parquet'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            # set up import object and pull from csv files
            nw = utils.ImportDataFromCSV(files)
            nw.get_data_from_csv()

            # group by asset/columns and create xref
            count_df = nw.get_num_columns_per_asset()
            asset_xref = count_df.to_dict()

            # add data to models
            for key, val in asset_xref:
                obj, create_asset = Asset.objects.get_or_create(
                    asset=key
                )
                Column.objects.create(
                    column=val,
                    asset=obj
                )

            # setup parquet files object, pivot data, and save
            pq = utils.ParquetFiles(self.pq_path)
            pq.data_frame = nw.pivot_dataframe()
            pq.save_dataframe_to_parquet()
            return render(
                request,
                self.template_name,
                {'form': None, 'path': self.pq_path}
            )

        return render(request, self.template_name, {'form': form})


class PlotDataView(TemplateView):
    template_name = 'plot.html'
    pq_path = conf_settings.PARQUET_FILES_DIR / 'nwave.parquet'

    def get(self, request, *args, **kwargs):
        # setup parquet files object and pull all data
        pq = utils.ParquetFiles(self.pq_path)
        df = pq.parquet_files_to_dataframe()

        # get unique assets, dates, and columns
        assets = list(df.asset.unique())
        dates = set(d.split(' ')[0] for d in df.timestamp.unique())
        dates = sorted(list(dates))
        exclude = ('timestamp', 'asset', 'year', 'month')
        columns = list((c for c in df.columns.values if c not in exclude))

        # render template
        json_dict = {'assets': assets, 'columns': columns, 'dates': dates}
        return render(
            request, self.template_name, {'data': json.dumps(json_dict)}
        )


class ParquetGetView(views.APIView):
    pq_path = conf_settings.PARQUET_FILES_DIR / 'nwave.parquet'

    def get(self, request):
        pq = utils.ParquetFiles(
            self.pq_path,
            asset=request.query_params.get('asset', ''),
            column=request.query_params.get('column', ''),
            beg_date=request.query_params.get('beg_date', ''),
            end_date=request.query_params.get('end_date', '')
        )
        records_data = pq.parquet_to_records_dictionary()
        return Response({'data': records_data})


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all().order_by('asset')
    serializer_class = AssetSerializer


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all().order_by('column')
    serializer_class = ColumnSerializer

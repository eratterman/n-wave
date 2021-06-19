from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .serializers import AssetSerializer, ColumnSerializer
from .models import Asset, Column
from .forms import FileFieldForm
from django.conf import settings as conf_settings
from rest_framework import views
from rest_framework.response import Response
from . import utils
import datetime
import json


class ImportFilesView(FormView):
    form_class = FileFieldForm
    template_name = 'import.html'
    pq_name = 'nwave.parquet'
    pq_path = conf_settings.PARQUET_FILES_DIR
    pq_file = pq_path / pq_name

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            # set up import object
            nw = utils.ImportDataFromCSV(files)
            # pull data from csv files into dataframe
            nw.get_data_from_csv()
            # get unique counts of columns by assets
            count_df = nw.get_num_columns_per_asset()
            # create cross reference of asset and column
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

            # setup parquet files object
            pq = utils.ParquetFiles(self.pq_file)
            # pivot data and set pfiles dataframe
            pq.data_frame = nw.pivot_dataframe()
            # save data to partitioned parquet file
            pq.save_dataframe_to_parquet()
            return render(
                request,
                self.template_name,
                {'form': None, 'path': self.pq_file}
            )

        return render(request, self.template_name, {'form': form})


class PlotDataView(TemplateView):
    template_name = 'plot.html'
    pq_name = 'nwave.parquet'
    pq_path = conf_settings.PARQUET_FILES_DIR
    pq_file = pq_path / pq_name

    def get(self, request, *args, **kwargs):
        # setup parquet files object and pull all data
        pq = utils.ParquetFiles(self.pq_file)
        df = pq.parquet_files_to_dataframe()
        assets = list(df.asset.unique())
        dates = sorted(list(set(
            datetime.date.strftime(
                d, '%Y-%m-%d'
            ) for d in df.timestamp.unique()
        )))
        columns = list((
            c for c in df.columns.values if c not in (
                'timestamp', 'asset', 'year', 'month'
            )
        ))
        json_dict = {'assets': assets, 'columns': columns, 'dates': dates}
        return render(
            request,
            self.template_name,
            {'data': json.dumps(json_dict)}
        )


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all().order_by('asset')
    serializer_class = AssetSerializer


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all().order_by('column')
    serializer_class = ColumnSerializer


# class ParquetGetView(views.APIView):
#     pq_name = 'nwave.parquet'
#     pq_path = conf_settings.PARQUET_FILES_DIR
#     pq_file = pq_path / pq_name
#
#     def get(self, request):
#         # pull query parameters
#         asset = request.query_params.get('asset', '')
#         column = request.query_params.get('column', '')
#         beg_date = request.query_params.get('beg_date', '')
#         end_date = request.query_params.get('end_date', '')
#
#     # setup parquet files object and pull all data
#     pq = utils.ParquetFiles(pq_path)
#     df = pq.parquet_files_to_dataframe()
#
#     # filter df and return json

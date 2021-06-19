import os
import time
import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path


class ImportDataFromCSV(object):
    def __init__(self, csv_files):
        self.csv_files = csv_files
        self.df = None
        self.pivoted = None

    def get_data_from_csv(self):
        frames = []
        for csv_file in yield_csv_file_rows(self.csv_files):
            # read data from csv
            df = pd.read_csv(csv_file)
            df.fillna('', inplace=True)

            # convert timestamp to datetime
            # df['timestamp'] = pd.to_datetime(df['timestamp'])

            # extract tag column
            df[['empty', 'site', 'asset', 'column']] = df['tag'].str.split(
                '/', expand=True
            )

            # remove empty column and add dataframe to list
            del df['empty']
            frames.append(df)

        # combine dataframes and return
        self.df = pd.concat(frames)
        return self.df

    def get_num_columns_per_asset(self):
        if self.df is None:
            self.get_data_from_csv()

        return self.df.groupby(['asset', 'column']).size()

    def pivot_dataframe(self):
        if self.df is None:
            self.get_data_from_csv()

        self.df.groupby('asset').cumcount()
        self.pivoted = self.df.pivot(
            index=['timestamp', 'asset'],
            columns='column',
            values='value'
        )
        self.pivoted.reset_index(inplace=True)
        return self.pivoted


class ParquetFiles(object):
    def __init__(self, file_path, **kwargs):
        self.file_path = file_path
        self.asset = kwargs.get('asset', '')
        self.column = kwargs.get('column', '')
        self.beg_date = kwargs.get('beg_date', '')
        self.end_date = kwargs.get('end_date', '')
        self.data_frame = None
        # self.options_xref = {
        #     'asset': kwargs.get('asset', ''),
        #     'column': kwargs.get('column', ''),
        #     'beg_date': kwargs.get('beg_date', ''),
        #     'end_date': kwargs.get('end_date', '')
        # }

    def save_dataframe_to_parquet(self):
        if self.data_frame is None:
            print(f'please set obj.data_frame - <pandas dataframe object>')
            return None

        self.data_frame['year'] = pd.DatetimeIndex(
            self.data_frame['timestamp']
        ).year
        self.data_frame['month'] = pd.DatetimeIndex(
            self.data_frame['timestamp']
        ).month
        table = pa.Table.from_pandas(self.data_frame)
        pq.write_to_dataset(
            table,
            root_path=self.file_path,
            partition_cols=['asset', 'year', 'month']
        )
        return self.data_frame

    def parquet_files_to_dataframe(self):
        filters = []
        if self.asset:
            filters.append(('asset', '==', self.asset))

        if self.column:
            filters.append(('column', '!=', ''))

        if self.beg_date:
            filters.append(('timestamp', '>=', self.beg_date))

        if self.end_date:
            filters.append(('timestamp', '<=', self.end_date))
        # for key, val in self.options_xref.items():
        #     if not val:
        #         continue
        #
        #     if key == 'column':
        #         filters.append((val, '!=', ''))
        #     elif key == 'asset':
        #         filters.append((key, '==', val))
        #     elif key == 'beg_date':
        #         filters.append(('timestamp', '>=', val))
        #     else:
        #         filters.append(('timestamp', '<=', val))

        if not filters:
            dataset = pq.ParquetDataset(self.file_path)
        else:
            dataset = pq.ParquetDataset(
                self.file_path,
                filters=filters
            )

        self.data_frame = dataset.read_pandas().to_pandas()
        return self.data_frame

    def parquet_to_records_dictionary(self):
        # get filtered dataframe
        filtered = self.parquet_files_to_dataframe()

        # filter out by date range
        if self.beg_date and self.end_date:
            after_start_date = filtered["timestamp"] >= self.beg_date
            before_end_date = filtered["timestamp"] <= self.end_date
            between_two_dates = after_start_date & before_end_date
            filtered = filtered.loc[between_two_dates]

        # copy columns to new dataframe and return records dictionary
        new_df = filtered[['timestamp', 'asset', self.column]].copy()
        return new_df.to_dict('records')


def yield_csv_file_rows(csv_list):
    for csv in csv_list:
        yield csv


if __name__ == '__main__':
    bt = time.perf_counter()

    # # set base and parquet out files path
    # base_path = Path(r'D:\dev\django\narrativewave\n-wave')
    # path_to_csv_files = base_path / 'challenge_datasets'
    # pq_path = base_path / 'parquet_files'
    # os.makedirs(pq_path, 0o777, exist_ok=True)
    # pq_file = pq_path / 'nwave.parquet'

    # csv_file_list = os.listdir(path_to_csv_files)
    # csv_file_list = list((
    #     path_to_csv_files / f for f in csv_file_list
    # ))

    # nw = ImportDataFromCSV(csv_file_list)
    # nw_df = nw.get_data_from_csv()
    # counts = nw.get_num_columns_per_asset()
    # asset_xref = counts.to_dict()
    # print(f'num assets: {len(asset_xref)}')
    # for key, val in asset_xref.items():
    #     print(f'asset: {key} - col: {val}')
    #

    # start_date = '2020-10-03 00:00:00'
    # end_date = '2020-10-03 23:59:59'
    # pq_df = ParquetFiles(
    #     pq_file,
    #     asset='WTG11',
    #     column='TimeStamp',
    #     beg_date=start_date,
    #     end_date=end_date
    # )
    # df = pq_df.parquet_files_to_dataframe()
    # print(df) # [113 rows x 65 columns]

    # filtered = df[df['asset'] == 'WTG11']
    # print(filtered)
    #
    #
    # after_start_date = df["timestamp"] >= start_date
    # before_end_date = df["timestamp"] <= end_date
    # between_two_dates = after_start_date & before_end_date
    # filtered = df.loc[between_two_dates]
    # print(filtered)
    #
    # columns = ['timestamp', 'asset', 'Gen_RPM_Avg']
    # new_df = filtered[columns].copy()
    # out_data = new_df.to_dict('records')
    # print(out_data)
    # pq_file = nw.save_dataframe_to_parquet(str(pq_file))
    # print('got pivoted data')
    # print(f'parquet file: {pq_file}')

    et = time.perf_counter()
    print(round(et - bt, 2))

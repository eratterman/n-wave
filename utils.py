import os
import time
import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path


class ImportDataFromCSV(object):
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.pivoted = None

    def get_data_from_csv(self):
        frames = []
        for csv_file in yield_csv_file_rows(self.csv_path):
            # read data from csv
            df = pd.read_csv(csv_file)
            df.fillna('', inplace=True)

            # convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

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

    def save_dataframe_to_parquet(self, pq_file_path):
        if self.pivoted is None:
            self.pivot_dataframe()

        self.pivoted['year'] = pd.DatetimeIndex(self.pivoted['timestamp']).year
        self.pivoted['month'] = pd.DatetimeIndex(self.pivoted['timestamp']).month
        table = pa.Table.from_pandas(self.pivoted)
        pq.write_to_dataset(
            table,
            root_path=pq_file_path,
            partition_cols=['asset', 'year', 'month']
        )
        return pq_file_path


def yield_csv_file_rows(file_path):
    csv_list = list((
        str(file_path / f) for f in os.listdir(file_path)
    ))
    for csv in csv_list:
        yield csv


if __name__ == '__main__':
    bt = time.perf_counter()

    # set base and parquet out files path
    base_path = Path(os.path.abspath(os.getcwd()))
    path_to_csv_files = base_path / 'challenge_datasets'
    pq_path = base_path / 'parquet_files'
    os.makedirs(pq_path, 0o777, exist_ok=True)
    pq_file = pq_path / 'test.parquet'

    # nwave = ImportDataFromCSV(path_to_csv_files)
    # nw_df = nwave.get_data_from_csv()
    # counts = nwave.get_num_columns_per_asset()
    # nwave.pivot_dataframe()
    # pq_file = nwave.save_dataframe_to_parquet(str(pq_file))
    # print('got pivoted data')
    # print(f'parquet file: {pq_file}')
    #

    pq.ParquetFile(pq_file)

    # dataset = pq.ParquetDataset(
    #     pq_file,
    #     filters=[('asset', '=', 'WTG01')]
    # )
    # df = dataset.to_table(
    #     columns=['timestamp', 'asset', 'column'],
    #     use_threads=True
    # ).to_pandas()

    et = time.perf_counter()
    print(round(et - bt, 2))

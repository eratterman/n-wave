import os
import time
import pandas as pd
from pathlib import Path


class ImportCSV(object):
    def __init__(self):
        self.base_path = Path(os.path.abspath(os.getcwd()))
        self.pq_path = self.base_path / 'parquet_files'
        self.csv_path = self.base_path / 'challenge_datasets'
        os.makedirs(self.pq_path, 0o777, exist_ok=True)

    def get_data_from_csv(self):
        frames = []
        for csv_file in get_csv_files(self.csv_path):
            # print(csv_file)
            df = pd.read_csv(csv_file)
            df.fillna('', inplace=True)

            # # convert timestamp to datetime
            # df['timestamp'] = pd.to_datetime(df['timestamp'])

            # extract tag column
            df[['empty', 'site', 'asset', 'column']] = df['tag'].str.split(
                '/', expand=True
            )

            # remove empty column and add dataframe to list
            del df['empty']
            frames.append(df)

        # return combined dataframes
        return pd.concat(frames)


def get_csv_files(file_path):
    csv_list = list((
        str(file_path / f) for f in os.listdir(file_path)
    ))
    for csv in csv_list:
        yield csv


if __name__ == '__main__':
    bt = time.perf_counter()

    # set base and parquet out files path
    base_path = Path(os.path.abspath(os.getcwd()))
    pq_path = base_path / 'parquet_files'
    os.makedirs(pq_path, 0o777, exist_ok=True)

    # pull data from csv files into dataframe
    n_wave_df = get_data_from_csv(base_path)

    # all_csv_data = get_data_from_csv(base_path)
    # site_name = all_csv_data.site.unique()
    # n_wave_df = all_csv_data[
    #     ['timestamp', 'asset', 'column', 'value']
    # ].copy()
    print(f'got all data')
    # pivot on asset
    # n_wave_df.groupby('tag').cumcount()
    # assets = n_wave_df.asset.unique()
    # cols = n_wave_df.column.unique()
    # print(assets, len(assets))
    # print(cols, len(cols))
    # n_wave_df.pivot_table(index='tag', columns='timestamp', values='value')
    # pd.set_option('display.max_rows', 5, 'display.max_columns', None)
    # print(n_wave_df)
    # exit()

    et = time.perf_counter()
    print(round(et - bt, 2))

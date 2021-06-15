import os
import time
import pandas as pd
from pathlib import Path


class ImportDataFromCSV(object):
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None

    def get_data_from_csv(self):
        frames = []
        for csv_file in yield_csv_file_rows(self.csv_path):
            # print(csv_file)
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

        # combine dataframes, pivot on timestamp/asset and return data
        self.df = pd.concat(frames)
        self.df.groupby('asset').cumcount()
        self.df = self.df.pivot(
            index=['timestamp', 'asset'],
            columns='column',
            values='value'
        )
        self.df.reset_index(inplace=True)
        return self.df


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
    # pq_path = base_path / 'parquet_files'
    # os.makedirs(pq_path, 0o777, exist_ok=True)

    nwave = ImportDataFromCSV(path_to_csv_files)
    nw_df = nwave.get_data_from_csv()
    print('got pivoted data')

    et = time.perf_counter()
    print(round(et - bt, 2))

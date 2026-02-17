'''Load raw data from GCS into BigQuery tables.'''

import os
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import bigquery


# ------- load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

GCS_BUCKET = os.environ['GCS_BUCKET']
BQ_DATASET = os.environ['BQ_DATASET']


# ------- tables to load (table_name, gcs_path, format, write_mode)
TRIP_TABLES = [
    ('yellow_trips', 'raw/yellow_trips_2020.parquet'),
    ('rideshare_trips', 'raw/rideshare_trips_2020.parquet'),
]

LOOKUP_TABLES = [
    ('taxi_zone_lookup', 'raw/taxi_zone_lookup.csv'),
]


def load_parquet_to_bq(table_name: str, gcs_path: str):
    '''Load a parquet file from GCS into BigQuery, appending to existing data.'''
    bq_client = bigquery.Client()
    table_id = f'{bq_client.project}.{BQ_DATASET}.{table_name}'
    gcs_uri = f'gs://{GCS_BUCKET}/{gcs_path}'

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    print(f'Loading {gcs_uri} -> {table_id}...')
    job = bq_client.load_table_from_uri(gcs_uri, table_id, job_config=job_config)
    job.result()

    table = bq_client.get_table(table_id)
    print(f'Loaded {table.num_rows:,} rows into {table_id}')


def load_csv_to_bq(table_name: str, gcs_path: str):
    '''Load a CSV file from GCS into BigQuery, replacing existing data.'''
    bq_client = bigquery.Client()
    table_id = f'{bq_client.project}.{BQ_DATASET}.{table_name}'
    gcs_uri = f'gs://{GCS_BUCKET}/{gcs_path}'

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    print(f'Loading {gcs_uri} -> {table_id}...')
    job = bq_client.load_table_from_uri(gcs_uri, table_id, job_config=job_config)
    job.result()

    table = bq_client.get_table(table_id)
    print(f'Loaded {table.num_rows:,} rows into {table_id}')


def main():
    for table_name, gcs_path in TRIP_TABLES:
        load_parquet_to_bq(table_name, gcs_path)

    for table_name, gcs_path in LOOKUP_TABLES:
        load_csv_to_bq(table_name, gcs_path)

    print('Done.')


if __name__ == '__main__':
    main()

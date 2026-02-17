'''Download 2020 NYC TLC trip data (Yellow Taxi + FHVHV), upload to GCS, and load into BigQuery.'''

import os
import httpx
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import bigquery, storage


# ------- load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

BASE_URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
LOOKUP_URL = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
DATASETS = {
    'yellow': 'yellow_tripdata',
    'rideshare': 'fhvhv_tripdata'
}
YEAR = 2020

GCS_BUCKET = os.environ['GCS_BUCKET']
BQ_DATASET = os.environ['BQ_DATASET']


def upload_to_gcs(local_path: Path, gcs_path: str) -> str:
    '''Upload a local file to GCS and return the gs:// URI.'''
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(str(local_path))
    uri = f'gs://{GCS_BUCKET}/{gcs_path}'
    print(f'Uploaded {local_path} -> {uri}')
    return uri


def load_gcs_to_bigquery(gcs_uri: str, table_id: str, source_format: str = 'PARQUET'):
    '''Load a file from GCS into a BigQuery table.'''
    client = bigquery.Client()
    full_table_id = f'{client.project}.{BQ_DATASET}.{table_id}'

    job_config = bigquery.LoadJobConfig(
        source_format=getattr(bigquery.SourceFormat, source_format),
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    if source_format == 'CSV':
        job_config.skip_leading_rows = 1
        job_config.autodetect = True

    job = client.load_table_from_uri(gcs_uri, full_table_id, job_config=job_config)
    job.result()
    table = client.get_table(full_table_id)
    print(f'Loaded {table.num_rows:,} rows into {full_table_id}')


def main():
    for label, prefix in DATASETS.items():
        monthly_files = []
        for month in range(1, 13):
            filename = f'{prefix}_{YEAR}-{month:02d}.parquet'
            dest = Path(filename)
            if not dest.exists():
                print(f'Downloading {filename}...')
                resp = httpx.get(
                    f'{BASE_URL}/{filename}',
                    follow_redirects=True,
                    timeout=60
                )
                resp.raise_for_status()
                dest.write_bytes(resp.content)
            monthly_files.append(dest)

        df = pd.concat([pd.read_parquet(f) for f in monthly_files])
        output = Path(f'{label}_trips_{YEAR}.parquet')
        df.to_parquet(output, compression='snappy')
        print(f'Wrote {output} ({len(df):,} rows)')

        for f in monthly_files:
            f.unlink()

        table_name = f'{label}_trips'
        gcs_uri = upload_to_gcs(output, f'raw/{output.name}')
        load_gcs_to_bigquery(gcs_uri, table_name)
        output.unlink()

    lookup = Path('taxi_zone_lookup.csv')
    if not lookup.exists():
        resp = httpx.get(LOOKUP_URL, follow_redirects=True, timeout=60)
        resp.raise_for_status()
        lookup.write_bytes(resp.content)

    gcs_uri = upload_to_gcs(lookup, f'raw/{lookup.name}')
    load_gcs_to_bigquery(gcs_uri, 'taxi_zone_lookup', source_format='CSV')
    lookup.unlink()

    print('Done.')


if __name__ == '__main__':
    main()

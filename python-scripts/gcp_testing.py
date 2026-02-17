

import os
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import storage, bigquery


# ------- load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

bucket_name = os.environ['GCS_BUCKET']
bq_dataset = os.environ['BQ_DATASET']
local_csv = Path(__file__).parent / 'test.csv'



# ------- test uploading local csv to gcs
gcs_client = storage.Client()
bucket = gcs_client.bucket(bucket_name)
blob = bucket.blob(f'test/{local_csv.name}')
blob.upload_from_filename(str(local_csv))

gcs_uri = f'gs://{bucket_name}/test/{local_csv.name}'

print(f'Uploaded {local_csv.name} to {gcs_uri}')



# ------- 
bq_client = bigquery.Client()
table_id = f'{bq_client.project}.{bq_dataset}.test_upload'

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
)

bq_load_job = bq_client.load_table_from_uri(
    gcs_uri,
    table_id,
    job_config=job_config
)
bq_load_job.result()  # wait for completion
table = bq_client.get_table(table_id)
print(f'Loaded {table.num_rows} rows into {table_id}')
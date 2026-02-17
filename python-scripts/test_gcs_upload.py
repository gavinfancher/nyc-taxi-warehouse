'''Quick test: upload test.csv to GCS bucket using .env from parent directory.'''

import os
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv(Path(__file__).resolve().parent.parent / '.env')

bucket_name = os.environ['GCS_BUCKET']
local_file = Path(__file__).resolve().parent / 'test.csv'

client = storage.Client()
bucket = client.bucket(bucket_name)
blob = bucket.blob(f'test/{local_file.name}')
blob.upload_from_filename(str(local_file))

print(f'Uploaded {local_file} -> gs://{bucket_name}/test/{local_file.name}')

"""🍍 Simulate concept drift: append viral-era data to the live dataset in S3."""
import io
import os
import boto3
import pandas as pd
from generate_data import generate

BUCKET = os.environ["BUCKET"]
s3 = boto3.client("s3", region_name="us-east-1")

obj = s3.get_object(Bucket=BUCKET, Key="data/orders.csv")
df = pd.read_csv(io.BytesIO(obj["Body"].read()))
print(f"Dataset before the incident: {len(df)} rows")

drifted = generate(era="pineapple", rows=500, seed=7)
df = pd.concat([df, drifted], ignore_index=True)

buf = io.StringIO()
df.to_csv(buf, index=False)
s3.put_object(Bucket=BUCKET, Key="data/orders.csv", Body=buf.getvalue())

print(
    f"🍍 THE INCIDENT HAS OCCURRED. Dataset now: {len(df)} rows "
    f"({len(drifted)} rows of viral pineapple madness appended)"
)
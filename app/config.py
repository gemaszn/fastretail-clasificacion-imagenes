import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "fastretail-product-images-gema")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "FastRetailImageClassifications")
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", 75))

if not S3_BUCKET_NAME:
    raise ValueError("Falta configurar S3_BUCKET_NAME en el archivo .env")
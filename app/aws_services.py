from decimal import Decimal
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from app.config import AWS_REGION, S3_BUCKET_NAME, DYNAMODB_TABLE_NAME, MIN_CONFIDENCE
from app.category_mapper import assign_category


s3_client = boto3.client("s3", region_name=AWS_REGION)
rekognition_client = boto3.client("rekognition", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def upload_image_to_s3(file_bytes: bytes, filename: str) -> tuple[str, str]:
    """
    Sube la imagen a S3 y devuelve el ID interno y la clave del objeto.
    """

    image_id = str(uuid.uuid4())
    extension = filename.split(".")[-1].lower()
    s3_key = f"products/{image_id}.{extension}"

    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_bytes,
            ContentType=f"image/{extension}"
        )
    except ClientError as error:
        raise RuntimeError(f"Error subiendo imagen a S3: {error}")

    return image_id, s3_key


def detect_labels_with_rekognition(s3_key: str) -> list[dict]:
    """
    Usa Amazon Rekognition para detectar etiquetas de una imagen almacenada en S3.
    """

    try:
        response = rekognition_client.detect_labels(
            Image={
                "S3Object": {
                    "Bucket": S3_BUCKET_NAME,
                    "Name": s3_key
                }
            },
            MaxLabels=15,
            MinConfidence=MIN_CONFIDENCE
        )
    except ClientError as error:
        raise RuntimeError(f"Error analizando imagen con Rekognition: {error}")

    labels = []

    for label in response.get("Labels", []):
        labels.append({
            "Name": label["Name"],
            "Confidence": round(label["Confidence"], 2)
        })

    return labels


def convert_labels_to_dynamodb_format(labels: list[dict]) -> list[dict]:
    """
    Convierte los valores float de las etiquetas a Decimal,
    porque DynamoDB no acepta float directamente.
    """

    safe_labels = []

    for label in labels:
        safe_labels.append({
            "Name": label["Name"],
            "Confidence": Decimal(str(label["Confidence"]))
        })

    return safe_labels


def save_classification_result(
    image_id: str,
    filename: str,
    s3_key: str,
    labels: list[dict],
    assigned_category: str,
    confidence: float
) -> dict:
    """
    Guarda el resultado en DynamoDB.
    """

    safe_labels = convert_labels_to_dynamodb_format(labels)

    item = {
        "image_id": image_id,
        "filename": filename,
        "s3_bucket": S3_BUCKET_NAME,
        "s3_key": s3_key,
        "detected_labels": safe_labels,
        "assigned_category": assigned_category,
        "confidence": Decimal(str(round(confidence, 2))),
        "status": "classified" if assigned_category != "Sin categoría" else "review_required",
        "created_at": datetime.utcnow().isoformat()
    }

    try:
        table.put_item(Item=item)
    except ClientError as error:
        raise RuntimeError(f"Error guardando resultado en DynamoDB: {error}")

    return {
        "image_id": image_id,
        "filename": filename,
        "s3_bucket": S3_BUCKET_NAME,
        "s3_key": s3_key,
        "detected_labels": labels,
        "assigned_category": assigned_category,
        "confidence": round(confidence, 2),
        "status": "classified" if assigned_category != "Sin categoría" else "review_required",
        "created_at": item["created_at"]
    }


def process_product_image(file_bytes: bytes, filename: str) -> dict:
    """
    Pipeline completo:
    1. Sube imagen a S3.
    2. Analiza imagen con Rekognition.
    3. Asigna categoría automática.
    4. Guarda resultado en DynamoDB.
    """

    image_id, s3_key = upload_image_to_s3(file_bytes, filename)
    labels = detect_labels_with_rekognition(s3_key)

    assigned_category, confidence = assign_category(labels)

    result = save_classification_result(
        image_id=image_id,
        filename=filename,
        s3_key=s3_key,
        labels=labels,
        assigned_category=assigned_category,
        confidence=confidence
    )

    return result


def convert_dynamodb_decimals(item):
    """
    Convierte Decimal a float/string para que los datos de DynamoDB
    se puedan mostrar correctamente en la web y devolver como JSON.
    """

    if isinstance(item, list):
        return [convert_dynamodb_decimals(value) for value in item]

    if isinstance(item, dict):
        return {
            key: convert_dynamodb_decimals(value)
            for key, value in item.items()
        }

    if isinstance(item, Decimal):
        return float(item)

    return item


def get_classification_history() -> list[dict]:
    """
    Recupera el histórico de clasificaciones.
    """

    try:
        response = table.scan()
    except ClientError as error:
        raise RuntimeError(f"Error leyendo DynamoDB: {error}")

    items = response.get("Items", [])
    items = convert_dynamodb_decimals(items)

    items.sort(key=lambda item: item.get("created_at", ""), reverse=True)

    return items
import boto3
import os

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_S3_REGION")  # <-- cambia esto si usás AWS_REGION en .env
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def subir_imagen_a_s3(archivo, nombre_destino):
    s3.upload_fileobj(
        archivo,
        BUCKET_NAME,
        nombre_destino,
        ExtraArgs={'ACL': 'public-read', 'ContentType': archivo.content_type}
    )
    url = f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{nombre_destino}"
    return url

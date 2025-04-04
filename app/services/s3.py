import boto3
from flask import current_app

def subir_imagen_a_s3(archivo, nombre_destino):
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
        region_name=current_app.config['AWS_REGION']
    )

    bucket_name = current_app.config['S3_BUCKET_NAME']

    s3.upload_fileobj(
        archivo,
        bucket_name,
        nombre_destino,
        ExtraArgs={'ContentType': archivo.content_type}  # ❌ Quitamos 'ACL': 'public-read'
    )

    url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{nombre_destino}"
    return url

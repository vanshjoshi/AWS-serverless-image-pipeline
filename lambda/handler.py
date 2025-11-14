import boto3
from PIL import Image
import io
import os
import urllib.parse

s3 = boto3.client('s3')
sns = boto3.client('sns')

OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    try:
        # --- BUCKET AND KEY ---
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        encoded_key = event['Records'][0]['s3']['object']['key']
        source_key = urllib.parse.unquote_plus(encoded_key)

        print("SOURCE BUCKET:", source_bucket)
        print("SOURCE KEY:", source_key)

        # --- DOWNLOAD ORIGINAL IMAGE ---
        obj = s3.get_object(Bucket=source_bucket, Key=source_key)
        img_data = obj['Body'].read()
        img = Image.open(io.BytesIO(img_data))

        # Base file name (without extension)
        base_name = source_key.rsplit('.', 1)[0]

        # --- SIZES ---
        sizes = {
            "small": (300, 300),
            "medium": (600, 600),
            "large": (1200, 1200)
        }

        # --- CREATE 3 RESIZED JPG FILES ---
        for size_name, dimensions in sizes.items():
            print(f"Processing {size_name}: {dimensions}")

            resized = img.copy()
            resized = resized.resize(dimensions)

            buffer = io.BytesIO()
            resized.save(buffer, format="JPEG", optimize=True, quality=85)
            buffer.seek(0)

            output_key = f"{base_name}_{size_name}.jpg"

            s3.put_object(
                Bucket=OUTPUT_BUCKET,
                Key=output_key,
                Body=buffer,
                ContentType='image/jpeg'
            )

            print("SAVED JPG:", output_key)

        # --- CREATE PDF ---
        pdf_buffer = io.BytesIO()
        img.convert("RGB").save(pdf_buffer, format="PDF", optimize=True, quality=85)
        pdf_buffer.seek(0)

        pdf_key = f"{base_name}.pdf"

        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=pdf_key,
            Body=pdf_buffer,
            ContentType="application/pdf"
        )

        print("PDF CREATED:", pdf_key)

        # --- SNS SUCCESS ---
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=(
                f"SUCCESS: {source_key} processed.\n"
                f"Generated: small, medium, large JPG + PDF"
            ),
            Subject="Image Processing Successful"
        )

        return {
            "statusCode": 200,
            "body": "Processing completed successfully."
        }

    except Exception as e:
        error_message = str(e)
        print("ERROR:", error_message)

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"FAILED to process file.\nError: {error_message}",
            Subject="Image Processing Failed"
        )

        raise e


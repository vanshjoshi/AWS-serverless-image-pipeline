🚀 Serverless Image Processing Pipeline (AWS Lambda • S3 • SNS)

A fully serverless, event-driven image processing pipeline built on AWS. This solution automatically processes images upon upload and delivers optimized outputs with real-time notifications — all without managing any servers.

In this video, you'll learn the exact steps needed to run this project successfully
https://www.youtube.com/watch?v=cSz3Ei7Kg7U

📌 Architecture Overview

Workflow:

A user uploads an image to the input S3 bucket.

An S3 event trigger invokes the AWS Lambda function.

Lambda performs:

Image resizing (three sizes: small, medium, large)

PDF generation (compressed)

Upload of output files to a destination S3 bucket

SNS notification for success or failure

SNS sends an SMS or email alert.

Components:

S3 (input-bkt-irs) – Source bucket for image uploads

AWS Lambda – Image processing logic

S3 (output-bkt-irs) – Stores resized JPGs and compressed PDF

SNS Topic – Sends processing status notifications

✨ Features
🖼 Intelligent Image Processing

Automatically generates optimized JPG versions:

300×300px — Small

600×600px — Medium

1200×1200px — Large

📄 PDF Generation

Converts the original image into a compressed, high-quality PDF

Reduces storage cost while maintaining clarity

🔔 Notification System (SNS)

Sends SMS/Email alerts

Includes success or detailed failure information

🧱 Fully Serverless Architecture

100% event-driven

Auto-scaling

No EC2 instances or manual provisioning required

📈 Production-Ready Build

Structured logging

Robust error handling

Principle of Least Privilege (IAM)

Highly scalable and extendable

📁 Repository Structure
serverless-image-pipeline/
│
├── lambda/
│ ├── handler.py # Main AWS Lambda function
│ └── requirements.txt # Python dependencies (e.g., Pillow)
│
├── .gitignore
├── LICENSE
└── README.md
🛠 Deployment Guide
1️⃣ Create S3 Buckets

input-bkt-irs

output-bkt-irs

2️⃣ Create SNS Topic

Name example: image-processing-status

Subscribe email or phone to receive notifications.

3️⃣ Create AWS Lambda Function

Runtime: Python 3.12

Memory: 1024 MB

Timeout: 180 seconds

Layers: Attach PillowLayerPython313

Environment Variables:

Key	Value
OUTPUT_BUCKET	output-bkt-irs
SNS_TOPIC_ARN	arn:aws:sns:::image-processing-status
🔐 IAM Role Requirements

Attach to Lambda execution role:

AWSLambdaBasicExecutionRole

AmazonS3FullAccess (or a restricted S3 policy)

AmazonSNSFullAccess

4️⃣ Add S3 Trigger

Service: S3

Bucket: input-bkt-irs

Event Type: PUT (Object Created)

Enable Trigger

🧪 Testing the Pipeline

Upload a .jpg or .png file to:

input-bkt-irs

Expected outputs in output-bkt-irs:

image_small.jpg

image_medium.jpg

image_large.jpg

image.pdf (compressed)

Expected SNS Notification:
SUCCESS: yourfile.jpg processed successfully.
Generated: small, medium, large JPGs + compressed PDF

you can watch this video and follow all the steps: https://www.youtube.com/watch?v=cSz3Ei7Kg7U

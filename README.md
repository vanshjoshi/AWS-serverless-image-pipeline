🚀 Serverless Image Processing Pipeline (AWS Lambda + S3 + SNS)

A fully serverless, event-driven image processing system built on AWS.
When a user uploads an image to an S3 bucket, the system automatically:

✔ Generates 3 resized JPG versions
✔ Creates a compressed PDF
✔ Stores all outputs in a separate S3 bucket
✔ Sends an SNS Notification (SMS/Email) on success or failure
✔ Works 100% serverless — no servers to manage

This project is perfect for Cloud Engineer / DevOps Engineer portfolios.

📌 Architecture Overview
┌──────────────────┐       ┌───────────────────────────┐
│  input-bkt-irs    │──────▶│  AWS Lambda Function      │
│ (Upload Image)    │ S3    │  - Resizes Image          │
└──────────────────┘ Event  │  - Creates PDF            │
                            │  - Uploads outputs        │
                            │  - Sends SNS Notification │
                            └───────────┬───────────────┘
                                        │
                        ┌───────────────▼────────────────┐
                        │     output-bkt-irs (S3)         │
                        │  small, medium, large JPGs      │
                        │  compressed PDF                 │
                        └─────────────────────────────────┘
                                        │
                        ┌───────────────▼────────────────┐
                        │            SNS Topic            │
                        │  SMS/Email on Success/Failure   │
                        └─────────────────────────────────┘

✨ Features
🖼 Advanced Image Processing

Resize image into:

300x300 (small)

600x600 (medium)

1200x1200 (large)

📄 PDF Generation

Converts original image into high-quality PDF

Compressed for low storage cost

🔔 Notification System

Sends SMS/email via SNS Topic

Includes success or failure details

🧱 Fully Serverless

No EC2 instances

Fully event-driven via S3 triggers

Automatic scaling

📈 Production Ready

Logging

Error handling

Scalable design

IAM permissions best practices

🧩 Repository Structure
serverless-image-pipeline/
│
├── lambda/
│   ├── handler.py           # Main Lambda code
│   └── requirements.txt     # Python dependencies
│
├── .gitignore
├── LICENSE
└── README.md

🛠 AWS Setup Instructions
1️⃣ Create S3 buckets
input-bkt-irs
output-bkt-irs

2️⃣ Create SNS Topic

Name example:

image-processing-status


Subscribe your phone/email to get notifications.

3️⃣ Create Lambda Function

Runtime → Python 3.12

Memory → 1024 MB

Timeout → 180 seconds

Attach Pillow Layer → PillowLayerPython313

Add environment variables:

Key	Value
OUTPUT_BUCKET	output-bkt-irs
SNS_TOPIC_ARN	arn:aws:sns:<region>:<account-id>:image-processing-status
🔐 IAM Permissions Required

Attach these to the Lambda execution role:

AWSLambdaBasicExecutionRole

AmazonS3FullAccess (or restricted S3 policy)

AmazonSNSFullAccess

🔔 Add S3 Trigger

Go to Lambda → Add Trigger:

Service: S3

Bucket: input-bkt-irs

Event Type: PUT

Enable Trigger

💻 Lambda Code (Already Included)

Located in:

lambda/handler.py

🧪 Testing

Upload any .jpg or .png file to:

input-bkt-irs


Expected outputs in output-bkt-irs:

photo_small.jpg
photo_medium.jpg
photo_large.jpg
photo.pdf


Expected SNS Notification:

SUCCESS: yourfile.jpg processed.
Generated: small, medium, large JPG + PDF


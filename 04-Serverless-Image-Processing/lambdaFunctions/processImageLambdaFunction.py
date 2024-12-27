import boto3
from urllib.parse import unquote

def lambda_handler(event, context):
    # Log the event for debugging
    print(f"Event: {event}")

    # Check if the event contains the 'detail' key
    if 'detail' not in event:
        print("Error: Event does not contain 'detail'")
        return {
            'statusCode': 400,
            'body': "Invalid event structure. 'detail' key is missing."
        }

    # Extract the S3 bucket name and object key from the EventBridge event
    try:
        s3_bucket = event['detail']['bucket']['name']
        s3_key = unquote(event['detail']['object']['key'])
        print(f"Bucket: {s3_bucket}, Key: {s3_key}")
    except KeyError as e:
        print(f"Error: Missing key in event - {e}")
        return {
            'statusCode': 400,
            'body': f"Invalid event structure. Missing key: {e}"
        }

    # Initialize the Rekognition client
    rekognition = boto3.client('rekognition', region_name='us-east-1')

    # Call Rekognition to detect faces
    try:
        response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
            Attributes=['ALL']
        )
        print(f"Rekognition Response: {response}")
        face_detected = len(response['FaceDetails']) > 0
        return {
            'statusCode': 200,
            'body': {
                's3_key': s3_key,
                'face_detected': face_detected
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': f"Error processing image: {e}"
        }

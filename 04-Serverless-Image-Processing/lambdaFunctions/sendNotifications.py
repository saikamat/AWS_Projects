import boto3
import json

def lambda_handler(event, context):
    # Log the event for debugging
    print(f"Event: {event}")

    # Initialize the SNS client
    sns = boto3.client('sns', region_name='us-east-1')

    # Extract details from the event (passed by Step Functions)
    try:
        # image_id = event.get('ImageID', 'Unknown Image')
        # face_detected = event.get('FaceDetected', False)
        # Access the 'body' key
        body = event.get('body', {})
        image_id = body.get('s3_key', 'Unknown Image')
        face_detected = body.get('face_detected', False)
        print(f"image_id: {image_id}")
        message = f"Face detected in image: {image_id}" if face_detected else f"No face detected in image: {image_id}"
        print(f"Message to send: {message}")
    except Exception as e:
        print(f"Error extracting event details: {e}")
        return {
            'statusCode': 400,
            'body': f"Error extracting event details: {e}"
        }

    # Publish the message to the SNS topic
    try:
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:318960958846:ImageProcessingNotifications',  # Replace with your SNS Topic ARN
            Message=message,
            Subject="Image Processing Results"
        )
        print(f"Notification sent. Response: {response}")
        return {
            'statusCode': 200,
            'body': f"Notification sent: {message}"
        }
    except Exception as e:
        print(f"Error sending notification: {e}")
        return {
            'statusCode': 500,
            'body': f"Error sending notification: {e}"
        }
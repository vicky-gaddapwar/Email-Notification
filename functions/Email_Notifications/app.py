import json
import boto3
import os


EMAIL_TEMPLATE = """
Hello {recipient_name},

{body}

Best regards,
Your Team
"""

def lambda_handler(event, context):
    """
    Publishes a formatted message to an SNS topic. All email subscribers to the topic will receive the message via SES.
    Example event:
    {
        "topic_arn": "arn:aws:sns:ap-south-1:123456789012:MyTopic",
        "subject": "Test Email",
        "body": "This is a test email sent from Lambda using SNS.",
        "recipient_name": "John"
    }
    """
    try:
        data = event if isinstance(event, dict) else json.loads(event)
        topic_arn = data['topic_arn']
        subject = data.get('subject', 'No Subject')
        body = data.get('body', '')
        recipient_name = data.get('recipient_name', 'User')

        sns_client = boto3.client('sns', region_name=os.environ.get('AWS_REGION', 'ap-south-1'))
        message = EMAIL_TEMPLATE.format(subject=subject, recipient_name=recipient_name, body=body)
        sns_client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent via SNS!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending notification: {str(e)}')
        }

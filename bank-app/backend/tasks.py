from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "bank_tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379"),
)


@celery_app.task
def send_transaction_notification(user_id, amount, transaction_type):
    print(f"Sending notification to user {user_id} " f"{transaction_type} of ${amount}")

    # Later this could:
    # - send email
    # - send push notification
    # - write audit logs
    # - call another service

    return "Notification sent"


@celery_app.task
def send_registration_notification(username, email):
    print(f"Sending email confirmation to {email} Welcome: {username}")

    return "Email Verification Sent"

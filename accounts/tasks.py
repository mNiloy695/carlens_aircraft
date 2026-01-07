from celery import shared_task
from .utils import send_the_email
from django.conf import settings

@shared_task(bind=True)
def send_otp_email_task(self, subject, user_email, message, message_type='registration'):
    try:
        print(f"[TASK START] Sending email to: {user_email}")
        send_the_email(
            subject=subject,
            message=message,
            user_email=user_email
        )
        print(f"[TASK SUCCESS] Email sent to: {user_email}")
    except Exception as e:
        print(f"[TASK ERROR] Failed to send email to {user_email}: {e}")
        # retry the task after 60 seconds if it fails
        raise self.retry(exc=e, countdown=60)

@shared_task
def debug_env():
    print("[DEBUG ENV] EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
    return settings.EMAIL_HOST_USER

import logging

from billiard.exceptions import SoftTimeLimitExceeded
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.template import loader
from django.conf import settings
from mailjet_rest import Client

logger = logging.getLogger("celery")


@shared_task(bind=True, max_retries=3)
def send_email(self, subject, context, template, emails):
    if not settings.DISCARD_EMAIL_WHITE_LIST:
        recipients_cleaned = [recipient for recipient in emails if recipient in settings.EMAIL_WHITE_LIST]
        if not recipients_cleaned:
            logger.warning(f"White list blocked all recipients {emails}")
            return
        emails = recipients_cleaned

    mailjet = Client(auth=(settings.MAILJET_PUBLIC_KEY, settings.MAILJET_SECRET_KEY),
                     version=settings.MAILJET_API_VERSION)

    html_string = loader.render_to_string(template, context)
    # prepare data for email
    data = {
        "from": {
            'email': settings.MAILJET_ACCOUNT_EMAIL,
            'name': settings.MAILJET_NAME
        },
        "to": [emails],
        "subject": subject,
        "html": html_string
    }
    try:
        logger.info(f"Sending email to '{emails}'")
        result = mailjet.send.create(data=data)
    except SoftTimeLimitExceeded:
        logger.error(f"Email to {emails} timeout error!")
        return
    logger.info(f"Email notification sent to {emails}")
    if result.status_code != 200:
        error = result.json()
        logger.error(f"Connection error occurred while sending of email. "
                     f"Code: {error} - Message: {error}")
        try:
            self.retry(countdown=60)
        except MaxRetriesExceededError as e:
            logger.error(str(e))

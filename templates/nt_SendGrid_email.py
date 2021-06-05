import json

from sendgrid.helpers.mail import Mail, PlainTextContent
from sendgrid import SendGridAPIClient

SENDGRID_API_KEY = "REPLACE_SENDGRID_API_KEY"

FROM_EMAIL = "REPLACE_EMAIL_ID"

RECIPIENT_EMAILS = ["REPLACE_RECIPIENT_EMAILS"]

EMAIL_SUBJECT = "REPLACE_EMAIL_SUBJECT"

# basic_content not html content
EMAIL_CONTENT = PlainTextContent("REPLACE_CONTENT")


def SendEmails(
    api_key, from_email, recipient_emails, subject, plain_text_content
):
    """ Send a dynamic email to a list of email addresses

    :returns API response code
    :raises Exception e: raises an exception """

    # create Mail object and populate
    message = Mail(
        from_email=from_email,
        to_emails=recipient_emails,
        subject=subject,
        plain_text_content=plain_text_content,
    )

    try:
        mail_client = SendGridAPIClient(api_key)
        response = mail_client.send(message)
        code = response.status_code
        body = (response.body,)
        headers = response.headers

        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")

    except Exception as e:
        print("Error: {0}".format(e))

    return str(response.status_code)


if __name__ == "__main__":
    SendEmails(
        SENDGRID_API_KEY,
        FROM_EMAIL,
        RECIPIENT_EMAILS,
        EMAIL_SUBJECT,
        EMAIL_CONTENT,
    )

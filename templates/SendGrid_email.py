import json

from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient


FROM_EMAIL = "REPLACE_EMAIL_ID"

TEMPLATE_ID = "REPLACE_TEMPLATE_ID"

RECIPIENT_EMAILS = ["REPLACE_RECIPIENT_EMAILS"]

EMAIL_SUBJECT = "REPLACE_EMAIL_SUBJECT"

SENDGRID_API_KEY = "REPLACE_SENDGRID_API_KEY"

with open("dynamic_data.json", "r+") as fp:
    DYNAMIC_DATA = json.load(fp)


def SendEmails(
    dynamic_data, from_email, recepient_emails, subject, template_id
):
    """ Send a dynamic email to a list of email addresses

    :returns API response code
    :raises Exception e: raises an exception """

    # create Mail object and populate
    message = Mail(
        from_email=from_email, to_emails=recepient_emails, subject=subject
    )

    # pass custom values for HTML placeholders
    message.dynamic_template_data = dynamic_data

    message.template_id = template_id

    try:
        mail_client = SendGridAPIClient(template_id)
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
        DYNAMIC_DATA, FROM_EMAIL, RECIPIENT_EMAILS, EMAIL_SUBJECT, TEMPLATE_ID
    )

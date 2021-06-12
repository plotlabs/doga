from twilio.rest import Client


account_sid = "REPLACE_WITH_SID"
auth_token = "REPLACE_WITH_AUTH_TOKEN"

_from = "REPLACE_WITH_FROM"

# Specify country code with the phone numbers. ex. for india prefix +91
to = REPLACE_WITH_TO
message = "REPLACE_WITH_MESSAGE"


def send_sms(msg="Doga event occurred"):
    if not isinstance(to, list):
        print("Could not find any recipients. Please make sure a list of recipients are provided in the `to` "
              "variable.")

    client = Client(account_sid, auth_token)

    for number in to:
        msg = client.messages.create(body=msg, from_=_from, to=number)

        if msg.error_code is not None:
            print("ERROR " + msg.error_message)

        else:
            print("Successfully send SMS !")
    return msg.sid


send_sms(message)

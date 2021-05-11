from twilio.rest import Client


account_sid = REPLACE_WITH_SID
auth_token = REPLACE_WITH_AUTH_TOKEN

_from = REPLACE_WITH_FROM
to = REPLACE_WITH_TO

message = REPLACE_WITH_MESSAGE


def send_sms(
    account_sid, auth_token, from_="", to=[], message="Doga event occured"
):
    client = Client(account_sid, auth_token)

    for number in to:
        message = client.messages.create(body=message, from_=_from, to=number)

        if message.error_code is not None:
            print("ERROR " + message.error_message)

    return message.sid


send_sms(account_sid, auth_token, _from, to, message)

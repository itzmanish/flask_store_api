from twilio.rest import Client
import os


FAILED_LOADING_API_KEY = 'Failed to load 2FACTOR api key'
SENDING_FAILED = 'Error in sending otp'


class OTPException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class OTP:
    account_sid = os.environ.get('TWILIO_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    @classmethod
    def send_otp(cls, phone: str, otp: str):

        if cls.account_sid and cls.auth_token is None:
            raise OTPException(FAILED_LOADING_API_KEY)

        client = Client(cls.account_sid, cls.auth_token)

        try:
            client.messages.create(
                body=f'{otp} is your OTP for phone verification at Flask rest store api. DO NOT Share this with anyone.',
                from_='+19283796242',
                to=phone
            )

        except Exception:
            raise OTPException(SENDING_FAILED)

import os
from requests import get

FAILED_LOADING_API_KEY = 'Failed to load 2FACTOR api key'
SENDING_FAILED = 'Error in sending otp'


class OTPException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class OTP:

    API_KEY = os.environ.get('2FACTOR_API_KEY')

    @classmethod
    def send_otp(cls, phone: str, otp: str):

        if cls.API_KEY is None:
            raise OTPException(FAILED_LOADING_API_KEY)

        try:
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = get(
                f'http://2factor.in/API/V1/{cls.API_KEY}/SMS/{phone}/{otp}',
                data=payload,
                headers=headers
            )

            print(response)

        except Exception as e:
            print(str(e))
            raise OTPException(SENDING_FAILED)

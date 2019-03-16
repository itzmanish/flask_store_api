import traceback
from time import time

from flask_restful import Resource

from libs.mailgun import MailGunException
from models.users import UserModel
from models.confirmation import ConfirmationModel
from utils import pretty_string, USER_NOT_FOUND
from schemas.confirmation import ConfirmationSchema

confirmation_schema = ConfirmationSchema()

ALREADY_CONFIRMED = 'Your account has been already confirmed.'
NOT_FOUND = 'No user associated with this confirmation id'
EXPIRED_ACTIVATION = 'The activation code is expired.'
CONFIRMED = 'Your account has been confirmed. '
RESEND_SUCCESSFUL = 'A confirmation link has been successfully re-sent to your registered email address.'
RESEND_FAILED = 'Confirmation link re-sent has been failed.'


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return pretty_string(NOT_FOUND), 404
        if confirmation.expired:
            return pretty_string(EXPIRED_ACTIVATION), 404
        if confirmation.confirmed:
            return pretty_string(ALREADY_CONFIRMED), 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        return pretty_string(CONFIRMED), 200


class ConfirmationByUser(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)

        if not user:
            return pretty_string(USER_NOT_FOUND), 404

        return (
            {
                'current_time': int(time()),
                'confirmation': [
                    confirmation_schema.dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
        )

    @classmethod
    def post(cls, user_id: int):
        user = UserModel.find_by_id(user_id)

        if not user:
            return pretty_string(USER_NOT_FOUND), 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return pretty_string(ALREADY_CONFIRMED), 400
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_mail()
            return pretty_string(RESEND_SUCCESSFUL), 201

        except MailGunException as e:
            return pretty_string(str(e)), 500

        except:
            traceback.print_exc()
            return pretty_string(RESEND_FAILED), 500

from core import ma
from models.confirmation import ConfirmationModel


class ConfirmationSchema(ma.ModelSchema):

    class Meta:
        model = ConfirmationModel
        load_only = ('user',)
        dump_only = ('id', 'expire_at', 'email_confirmed', 'otp_confirmed')
        include_fk = True

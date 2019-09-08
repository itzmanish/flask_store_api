from marshmallow import pre_dump, fields

from core import ma
from models.users import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ('password',)
        dump_only = ('id', 'confirmation', )

    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user


class UserPhoneSchema(ma.Schema):

    phone = fields.String(required=True, error_messages={
                          'required': 'Please provide phone number.'})

    class Meta:
        model = UserModel

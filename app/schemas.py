#Define your Marshmallow schemas here.

from marshmallow import Schema, fields

class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    email = fields.Email(required=False)

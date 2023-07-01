from marshmallow import Schema, fields


class LoginInputSchema(Schema):
    email = fields.Email(description="Email", load_default='ee-12@ya.ru')
    password = fields.Str(description="Password", load_default='superpass')


class OutputSchema(Schema):
    access_token = fields.Str(description="access_token", required=True)


class ErrorSchema(Schema):
    error = fields.Str(description="error", required=True)


class CreateUserSchema(Schema):
    name = fields.Str(description="Name", load_default='admin2')
    email = fields.Email(description="Email", load_default='ee-12@ya.ru')
    password = fields.Str(description="Password", load_default='superpass')
    password2 = fields.Str(description="Password", load_default='superpass')


class PostUrlSchema(Schema):
    url = fields.Str(description="Url", load_default='http://abc.hostname.com/somethings/anything/qqq12345678/?sodfdme_key=som2e_value&2wqeqwe=fsdgd2sf')


class PostUrlsSchema(Schema):
    file = fields.Str(metadata={"type": "file"}, allow_none=False)


class PostImageSchema(PostUrlsSchema):
    pass

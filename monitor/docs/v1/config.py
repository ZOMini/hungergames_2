from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

SWAGGER_URL = '/docs/v1'
API_URL = '/swagger/v1'
VERSION = '1.0.0'
CONFIG = {
    'layout': 'BaseLayout'
}


class APISpecSwagger(APISpec):
    def create_tags(self, tags: list[dict]):
        self.tag(*tags)

    def load_docstrings(self, app):
        for fn_name in app.view_functions:
            if fn_name != 'static':
                self.path(view=app.view_functions[fn_name])


apispec = APISpecSwagger(
    title='Flask Monitor documentation',
    version=VERSION,
    openapi_version='3.0.3',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# security
jwt_scheme = {
    'type': 'http', "scheme": 'bearer', 'bearerFormat': 'JWT',
    'description': 'Enter the token "abcde12345".',
}
apispec.components.security_scheme("jwt_key", jwt_scheme)

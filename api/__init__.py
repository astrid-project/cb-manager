from api.spec import Spec
from falcon import API
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from resource import routes
from schema.response import HTTPErrorSchema
from schema.query_request import QueryRequestSchema
from swagger_ui import falcon_api_doc
from utils.auth import auth


def api(title, version, dev_username, dev_password):
    instance = API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(auth(dev_username, dev_password)),
                             exempt_routes=['/api/doc', '/api/doc/swagger.json']),
        Marshmallow()
    ])
    api_spec = Spec(api=instance, title=title, version=version)
    routes(api=instance, spec=api_spec.get())
    falcon_api_doc(instance, config_path='./swagger/schema.json', url_prefix='/api/doc', title='API doc')
    api_spec.write()
    return instance

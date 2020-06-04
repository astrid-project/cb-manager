from document.exec_env import ExecEnvTypeDocument
from resource.base import BaseResource
from schema.exec_env import ExecEnvTypeSchema
from docstring import docstring


@docstring(method='get', sum='Execution Environment Type Read (Multiple)',
           desc='Get the list of execution environment types filtered by the query in the request body.',
           resp='List of execution environment types filtered by the query in the request body.')
@docstring(method='post', sum='Execution Environment Type Creation (Multiple)',
           desc='Create new execution environment types.', resp='Execution environment types created.')
@docstring(method='delete', sum='Execution Environment Type Delete (Multiple)',
           desc='Delete execution environment types filtered by the query in the request body.',
           resp='Execution environment types filtered by the query in the request body deleted.')
@docstring(method='put', sum='Execution Environment Type Update (Multiple)',
           desc='Update execution environment types.', resp='Execution environment types updated.')
class ExecEnvTypeResource(BaseResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
    routes = '/type/exec-env/'
    schema_cls = ExecEnvTypeSchema


@docstring(method='get', sum='Execution Environment Type Read (Single)',
           desc="""Get the execution environment type with the given `id` and filtered by the
                 query in the request body.""",
           resp='Execution environment type with the given `id` and filtered by the query in the request body.')
@docstring(method='post', sum='Execution Environment Type Creation (Single)',
           desc='Create new execution environment type with the given `id`.',
           resp='Execution environment type with the given `id` created.')
@docstring(method='delete', sum='Execution Environment Type Delete (Single)',
           desc="""Delete the execution environment type with the given `id` and filtered by
                   the query in the request body.""",
           resp="""Execution environment type with the given `id` and filtered by the query
                   in the request body deleted.""")
@docstring(method='put', sum='Execution Environment Type Update (Single)',
           desc='Update the execution environment type with the given `id`.',
           resp='Execution environment type with the given `id` updated.')
class ExecEnvTypeSelectedResource(ExecEnvTypeResource):
    routes = '/exec-env-type/{id}'

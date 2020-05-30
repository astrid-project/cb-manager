from document.exec_env.type import ExecEnvTypeDocument
from resource.base import BaseResource
from schema.exec_env.type import ExecEnvTypeSchema
from docstring import docstring


@docstring(method='get',
         sum='Execution Environment Type Read (Single)',
         desc="""Get the execution environment type with the given `id` and filtered by the
                 query in the request body.""",
          resp='Execution environment type with the given `id` and filtered by the query in the request body.')
@docstring(method='post',
         sum='Execution Environment Type Creation (Single)',
         desc='Create new execution environment type with the given `id`.',
         resp='Execution environment type with the given `id` created.')
@docstring(method='delete',
         sum='Execution Environment Type Delete (Single)',
         desc="""Delete the execution environment type with the given `id` and filtered by
                 the query in the request body.""",
         resp="""Execution environment type with the given `id` and filtered by the query
                 in the request body deleted.""")
@docstring(method='put',
         sum='Execution Environment Type Update (Single)',
         desc='Update the execution environment type with the given `id`.',
         resp='Execution environment type with the given `id` updated.')
class ExecEnvTypeSelectedResource(BaseResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
    routes = '/exec-env-type/{id}'
    schema_cls =ExecEnvTypeSchema


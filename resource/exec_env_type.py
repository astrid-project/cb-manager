import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text
from utils import docstring_parameter


class ExecEnvTypeDocument(Document):
    name = Text()

    class Index:
        name = 'exec-env-type'


@docstring_parameter(docstring='base', schema='ExecEnvTypeSchema', tag='exec-env-type',
                     get_summary='Execution Environment Type Read (Multiple)',
                     get_description='Get the list of execution environment types filtered by the query in the request body.',
                     get_responses_200_description='List of execution environment types filtered by the query in the request body.',
                     post_summary='Execution Environment Type Creation (Multiple)',
                     post_description='Create new execution environment types.',
                     post_responses_200_description='Execution environment types created.',
                     delete_summary='Execution Environment Type Delete (Multiple)',
                     delete_description='Delete execution environment types filtered by the query in the request body.',
                     delete_responses_200_description='Execution environment types filtered by the query in the request body deleted.',
                     put_summary='Execution Environment Type Update (Multiple)',
                     put_description='Update execution environment types.',
                     put_responses_200_description='Execution environment types updated.')
class ExecEnvTypeResource(BaseResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
    routes = '/config/exec-env-type', '/config/exec-env-type/{id}'


@docstring_parameter(docstring='selected', schema='ExecEnvTypeSchema', tag='exec-env-type',
                     get_summary='Execution Environment Type Read (Single)',
                     get_description='Get the execution environment type with the given `id` and filtered by the query in the request body.',
                     get_responses_200_description='Execution environment type with the given `id` and filtered by the query in the request body.',
                     post_summary='Execution Environment Type Creation (Single)',
                     post_description='Create new execution environment type with the given `id`.',
                     post_responses_200_description='Execution environment type with the given `id` created.',
                     delete_summary='Execution Environment Type Delete (Single)',
                     delete_description='Delete the execution environment type with the given `id` and filtered by the query in the request body.',
                     delete_responses_200_description='Execution environment type with the given `id` and filtered by the query in the request body deleted.',
                     put_summary='Execution Environment Type Update (Single)',
                     put_description='Update the execution environment type with the given `id`.',
                     put_responses_200_description='Execution environment type with the given `id` updated.')
class ExecEnvTypeSelectedResource(BaseResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
    routes = '/config/exec-env-type', '/config/exec-env-type/{id}'

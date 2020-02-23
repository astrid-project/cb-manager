from .base import BaseResource
from elasticsearch_dsl import Document, Text, Date
from utils import docstring_parameter


class ExecEnvDocument(Document):
    hostname = Text(required=True)
    type_id = Text(required=True)
    #started = Date(required=True) # TODO Not work

    class Index:
        name = 'exec-env'


@docstring_parameter(docstring='base', schema='ExecEnvSchema', tag='exec-env',
                     get_summary='Execution Environment Read (Multiple)',
                     get_description='Get the list of execution environments filtered by the query in the request body.',
                     get_responses_200_description='List of execution environments filtered by the query in the request body.',
                     post_summary='Execution Environment Creation (Multiple)',
                     post_description='Create new execution environments.',
                     post_responses_200_description='Execution environments created.',
                     delete_summary='Execution Environment Delete (Multiple)',
                     delete_description='Delete execution environments filtered by the query in the request body.',
                     delete_responses_200_description='Execution environments filtered by the query in the request body deleted.',
                     put_summary='Execution Environment Update (Multiple)',
                     put_description='Update execution environments.',
                     put_responses_200_description='Execution environments updated.')
class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
    routes = '/config/exec-env/'


@docstring_parameter(docstring='selected', schema='ExecEnvSchema', tag='exec-env',
                     get_summary='Execution Environment Read (Single)',
                     get_description='Get the execution environment with the given `id` and filtered by the query in the request body.',
                     get_responses_200_description='Execution environment with the given `id` and filtered by the query in the request body.',
                     post_summary='Execution Environment Creation (Single)',
                     post_description='Create a new execution environment with the given `id`.',
                     post_responses_200_description='Execution environment with the given `id` created.',
                     delete_summary='Execution Environment Delete (Single)',
                     delete_description='Delete the execution environment with the given `id` and filtered by the query in the request body.',
                     delete_responses_200_description='Execution environment with the given `id` and filtered by the query in the request body deleted.',
                     put_summary='Execution Environment Update (Single)',
                     put_description='Update the execution environment with the given `id`.',
                     put_responses_200_description='Execution environment with the given `id` updated.')
class ExecEnvSelectedResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
    routes = '/config/exec-env/{id}'

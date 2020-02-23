from .base import BaseResource
from elasticsearch_dsl import Document, Text, Date
from utils import docstring_parameter


class DataDocument(Document):
    exec_env_id = Text() # TODO
    agent_instance_id = Text() # TODO
    timestamp_event = Date() # TODO
    timestamp_agent = Date() # TODO

    class Index:
        name = 'data'


@docstring_parameter(docstring='base', schema='DataSchema', tag='data',
                     get_summary='Data Read (Multiple)',
                     get_description='Get the list of data filtered by the query in the request body.',
                     get_responses_200_description='List of data filtered by the query in the request body.',
                     post_summary='Data Insert (Multiple)',
                     post_description='Insert new data.',
                     post_responses_200_description='Data inserted.',
                     delete_summary='Data Delete (Multiple)',
                     delete_description='Delete data filtered by the query in the request body.',
                     delete_responses_200_description='Data filtered by the query in the request body deleted.',
                     put_summary='Data Update (Multiple)',
                     put_description='Update data.',
                     put_responses_200_description='Data updated.')
class DataResource(BaseResource):
    doc_cls = DataDocument
    doc_name = 'Data'
    routes = '/data/',


@docstring_parameter(docstring='selected', schema='DataSchema', tag='data',
                     get_summary='Data Read (Single)',
                     get_description='Get the data with the given `id` and filtered by the query in the request body.',
                     get_responses_200_description='Data with the given `id` and filtered by the query in the request body.',
                     post_summary='Data Insert (Single)',
                     post_description='Insert new data with the given `id`.',
                     post_responses_200_description='Data with the given `id` inserted.',
                     delete_summary='Data Delete (Single)',
                     delete_description='Delete data with the given `id` and filtered by the query in the request body.',
                     delete_responses_200_description='Data with the given `id` and filtered by the query in the request body deleted.',
                     put_summary='Data Update (Single)',
                     put_description='Update data with the given `id`.',
                     put_responses_200_description='Data with the given `id` updated.')
class DataSelectedResource(BaseResource):
    doc_cls = DataDocument
    doc_name = 'Data'
    routes = '/data/{id}',

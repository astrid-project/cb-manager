from document.data import DataDocument
from resource.base import BaseResource
from schema.data import DataSchema
from docstring import docstring


@docstring(method='get', sum='Data Read (Multiple)',
           desc='Get the list of data filtered by the query in the request body.',
           resp='List of data filtered by the query in the request body.')
@docstring(method='post', sum='Data Insert (Multiple)',
           desc='Insert new data.', resp='Data inserted.')
@docstring(method='delete', sum='Data Delete (Multiple)',
           desc='Delete data filtered by the query in the request body.',
           resp='Data filtered by the query in the request body deleted.')
@docstring(method='put', sum='Data Update (Multiple)',
           desc='Update data.', resp='Data updated.')
class DataResource(BaseResource):
    doc_cls = DataDocument
    doc_name = 'Data'
    routes = '/data/'
    schema_cls = DataSchema
    readonly_fields = ['agent_instance_id', 'ebpf_program_instance_id', 'timestamp_event', 'timestamp_agent']


@docstring(method='get', sum='Data Read (Single)',
           desc='Get the data with the given `id` and filtered by the query in the request body.',
           resp='Data with the given `id` and filtered by the query in the request body.')
@docstring(method='post', sum='Data Insert (Single)',
           desc='Insert new data with the given `id`.', resp='Data with the given `id` inserted.')
@docstring(method='delete', sum='Data Delete (Single)',
           desc='Delete data with the given `id` and filtered by the query in the request body.',
           resp='Data with the given `id` and filtered by the query in the request body deleted.')
@docstring(method='put', sum='Data Update (Single)',
           desc='Update data with the given `id`.', resp='Data with the given `id` updated.')
class DataSelectedResource(DataResource):
    routes = '/data/{id}'

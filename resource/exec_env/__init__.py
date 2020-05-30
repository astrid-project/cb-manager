from document.exec_env import ExecEnvDocument
from resource.base import BaseResource
from schema.exec_env import ExecEnvSchema
from schema.exec_env.type import ExecEnvTypeSchema
from docstring import docstring

@docstring(method='get',
         sum='Execution Environment Read (Multiple)',
         desc='Get the list of execution environments filtered by the query in the request body.',
         resp='List of execution environments filtered by the query in the request body.')
@docstring(method='post',
         sum='Execution Environment Creation (Multiple)',
         desc='Create new execution environments.',
         resp='Execution environments created.')
@docstring(method='delete',
         sum='Execution Environment Delete (Multiple)',
         desc='Delete execution environments filtered by the query in the request body.',
         resp='Execution environments filtered by the query in the request body deleted.')
@docstring(method='put',
         sum='Execution Environment Update (Multiple)',
         desc='Update execution environments.',
         resp='Execution environments updated.')
class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
    routes = '/exec-env/'
    schema_cls =ExecEnvSchema
    from resource.exec_env.heartbeat import heartbeat

    def __init__(self):
        super().__init__()
        self.heartbeat()

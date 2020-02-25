from .base import BaseResource

from args import Args
from datetime import datetime, timedelta
from elasticsearch_dsl import Date, Document, InnerDoc, Integer, Nested, Text
from http import HTTPStatus
from requests.auth import HTTPBasicAuth
from utils import docstring_parameter

import falcon
import hashlib
import requests
import threading
import utils


class LCPDocument(InnerDoc):
    port = Integer(required=True)
    username = Text()
    password = Text()
    cb_password = Text()
    cb_expiration = Date()
    last_heartbeat = Date()


class ExecEnvDocument(Document):
    hostname = Text(required=True)
    lcp = Nested(LCPDocument, required=True)
    type_id = Text(required=True)

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

    def __init__(self):
        super()
        self.heartbeat()

    def heartbeat(self):
        """
        Heartbeat procedure with the LCPs.
        """
        s = ExecEnvDocument.search()
        res = s.execute()
        for exec_env in res:
            try:
                lcp = exec_env.lcp
                lcp_cb_password = utils.generate_password()
                lcp.cb_password = utils.hash(lcp_cb_password)
                lcp.cb_expiration = utils.get_timestamp(datetime.now() + timedelta(seconds=Args.db.hb_period))
                auth = { 'username': lcp.username, 'password': lcp.password } if lcp.last_heartbeat else {}
                res = requests.post(f'http://{exec_env.hostname}:{lcp.port}/status',
                                    timeout=Args.db.hb_timeout,
                                    json={ 'id': exec_env.meta.id, **auth,
                                           'cb_password': lcp_cb_password,
                                           'cb_expiration': lcp.cb_expiration })
            except Exception as e:
                self.log.debug(e)
                lcp.last_heartbeat = None
                exec_env.save()
            else:
                try:
                    if res.status_code == HTTPStatus.OK:
                        data = res.json()
                        lcp.username = data.get('username', None)
                        lcp.password = data.get('password', None)
                        lcp.last_heartbeat = data.get('last_hearthbeat', None)
                        exec_env.save()
                    else:
                        lcp.last_heartbeat = None
                        exec_env.save()
                except Exception as e:
                    self.log.debug(e)
                    lcp.last_heartbeat = None
                    exec_env.save()
        t = threading.Timer(Args.db.hb_period, self.heartbeat)
        t.daemon = True
        t.start()


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

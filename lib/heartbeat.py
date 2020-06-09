from reader.arg import ArgReader
from datetime import datetime, timedelta
from document.exec_env import ExecEnvDocument
from http import HTTPStatus
from requests import post
from threading import Timer
from utils.datetime import datetime_to_str
from utils.hash import generate_password, hash
from utils.log import Log
from docstring import docstring


def heartbeat():
    """Heartbeat procedure with the LCPs."""
    log = Log.get('heartbeat')
    s = ExecEnvDocument.search()
    res = s.execute()
    for exec_env in res:
        try:
            id = exec_env.meta.id
            lcp = exec_env.lcp
            resp = post(f'http://{exec_env.hostname}:{lcp.port}/status',
                        timeout=ArgReader.db.hb_timeout,
                        json=dict(id=id, username=lcp.username, password=lcp.password))
            if resp.status_code == HTTPStatus.OK:
                data = resp.json()
                id = data.pop('id', None)
                lcp.started = data.get('started', None)
                lcp.last_heartbeat = data.get('last_heartbeat', None)
                lcp.username = data.get('username', None)
                lcp.password = data.get('password', None)
                log.success(f'LCP Connection with {id} established')
            else:
                log.warning(f'Reset LCP connection with {id}')
                log.notice(f'response: {resp.content}')
                lcp.username = lcp.password = lcp.last_heartbeat = None
        except Exception as exception:
            log.error(f'Exception: {exception}')
            lcp.username = lcp.password = lcp.last_heartbeat = None
        else:
            exec_env.save()
    t = Timer(ArgReader.db.hb_period, heartbeat)
    t.daemon = True
    t.start()

from reader.arg import ArgReader
from datetime import datetime, timedelta
from document.exec_env import ExecEnvDocument
from http import HTTPStatus
from requests import post
from threading import Timer
from utils.datetime import datetime_to_str
from utils.hash import generate_password, hash
from docstring import docstring


def heartbeat(self):
    """
    Heartbeat procedure with the LCPs.
    """
    s = ExecEnvDocument.search()
    res = s.execute()
    for exec_env in res:
        try:
            lcp = exec_env.lcp
            lcp_cb_password = generate_password()
            lcp.cb_password = hash(lcp_cb_password)
            lcp.cb_expiration = datetime_to_str(datetime.now() + timedelta(seconds=ArgReader.db.hb_auth_expiration))
            auth = dict(username=lcp.username, password=lcp.password) if lcp.last_heartbeat else {}
            resp = post(f'http://{exec_env.hostname}:{lcp.port}/status', timeout=ArgReader.db.hb_timeout,
                        json=dict(id=exec_env.meta.id, **auth, cb_password=lcp_cb_password,
                                cb_expiration=lcp.cb_expiration))
        except Exception as exception:
            self.log.error(f'Exception: {exception}')
            lcp.username = lcp.password = lcp.last_heartbeat = None
            exec_env.save()
        else:
            try:
                if resp.status_code == HTTPStatus.OK:
                    data = resp.json()
                    lcp.username = data.get('username', None)
                    lcp.password = data.get('password', None)
                    lcp.last_heartbeat = data.get('last_hearthbeat', None)
                    self.log.success(f'LCP Connection with id = {exec_env.meta.id} established')
                else:
                    self.log.warning(f'Reset LCP connection with id = {exec_env.meta.id}')
                    self.log.notice(f'response: {resp}')
                    lcp.username = lcp.password = lcp.last_heartbeat = None
            except Exception as exception:
                self.log.error(f'Exception: {exception}')
                lcp.username = lcp.password = lcp.last_heartbeat = None
            else:
                exec_env.save()
    t = Timer(ArgReader.db.hb_period, self.heartbeat)
    t.daemon = True
    t.start()

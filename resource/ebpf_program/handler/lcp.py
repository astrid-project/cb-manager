from document.ebpf_program.catalog import eBPF_Program_Catalog_Document
from document.exec_env import Exec_Env_Document
from lib.response import Unprocessable_Entity_Response
from requests import post as post_req, put as put_req, delete as delete_req
from requests.auth import HTTPBasicAuth as HTTP_Basic_Auth
from resource.base.handler.lcp import LCP as Base_LCP
from utils.log import Log

__all__ = [
    'LCP'
]


# FIXME parameters add to instance
# TODO check if work everything
class LCP(Base_LCP):
    def __init__(self, catalog, req, resp):
        self.log = Log.get('ebpf-program-instance-lcp')
        self.req = req
        self.resp = resp
        self.req_lcp = {}
        self.catalog = catalog

    @classmethod
    def post(cls, instance, req, resp):
        def __data(catalog):
            return dict(id=catalog.meta.id,
                        interface=req.get('interface', None),
                        **catalog.config.to_dict())
        cls.__handler(instance=instance, req=req, resp=resp,
                      caller=post_req, data=__data)

    @classmethod
    def put(cls, instance, req, resp):
        def __data(catalog):
            return dict(id=catalog.meta.id,
                        interface=req.get('interface', None),
                        **catalog.config.to_dict())
        cls.__handler(instance=instance, req=req, resp=resp,
                      caller=put_req, data=__data)

    @ classmethod
    def delete(cls, instance, req, resp):
        def __data(catalog):
            return dict(id=catalog.meta.id)
        cls.__handler(instance=instance, req=req, resp=resp,
                      caller=delete_req, data=__data)

    @ classmethod
    def __handler(cls, instance, req, resp, caller, data):
        ebpf_program_catalog = cls.from_doc(document=eBPF_Program_Catalog_Document, id=instance.ebpf_program_catalog_id,
                                            label='eBPF Program Catalog', resp=resp)
        exec_env = cls.from_doc(document=Exec_Env_Document, id=instance.exec_env_id,
                                label='Execution Environment', resp=resp)
        if all([ebpf_program_catalog, exec_env]):
            LCP(catalog=ebpf_program_catalog, req=req, resp=resp).__apply(instance=instance,
                                                                          exec_env=exec_env,
                                                                          caller=caller,
                                                                          data=data)

    def __apply(self, instance, exec_env, caller, data):
        h, p = exec_env.hostname, exec_env.lcp.port
        u, ps = exec_env.lcp.username, exec_env.lcp.password
        resp_caller = caller(f'http://{h}:{p}/code', auth=HTTP_Basic_Auth(u, ps),
                             json=data(self.catalog))
        if resp_caller.content:
            try:
                self.resp.append(resp_caller.json())
            except Exception as e:
                self.log.exception(e)
                msg = f'Response from LCP({exec_env.meta.id}@{exec_env.hostname}:{exec_env.lcp.port}) not valid'
                uer = Unprocessable_Entity_Response(msg, exception=e)
                self.resp.append(uer)
        else:
            msg = f'Request to LCP({exec_env.meta.id}@{exec_env.hostname}:{exec_env.lcp.port}) not executed'
            self.resp.append(Unprocessable_Entity_Response(msg))

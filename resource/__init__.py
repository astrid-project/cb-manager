from resource.agent.catalog import AgentCatalogResource, AgentCatalogSelectedResource
from resource.agent.instance import AgentInstanceResource, AgentInstanceSelectedResource

from resource.connection import ConnectionResource, ConnectionSelectedResource

from resource.data import DataResource, DataSelectedResource

from resource.ebpf_program.catalog import eBPFProgramCatalogResource, eBPFProgramCatalogSelectedResource
from resource.ebpf_program.instance import eBPFProgramInstanceResource, eBPFProgramInstanceSelectedResource

from resource.exec_env import ExecEnvResource, ExecEnvSelectedResource
from resource.exec_env.type import ExecEnvTypeResource, ExecEnvTypeSelectedResource

from resource.network_link import NetworkLinkResource, NetworkLinkSelectedResource
from resource.network_link.type import NetworkLinkTypeResource, NetworkLinkTypeSelectedResource

from utils.log import Log
from utils.sequence import wrap

db = (
    AgentCatalogResource, AgentCatalogSelectedResource,
    AgentInstanceResource, AgentInstanceSelectedResource,
    ConnectionResource, ConnectionSelectedResource,
    DataResource, DataSelectedResource,
    eBPFProgramCatalogResource, eBPFProgramCatalogSelectedResource,
    eBPFProgramInstanceResource, eBPFProgramInstanceSelectedResource,
    ExecEnvResource, ExecEnvSelectedResource,
    ExecEnvTypeResource, ExecEnvTypeSelectedResource,
    NetworkLinkResource, NetworkLinkSelectedResource,
    NetworkLinkTypeResource, NetworkLinkTypeSelectedResource
)

tags = []
for Resource in db:
    tags.append(Resource.tag)


def routes(api, spec):
    log = Log.get('resource')
    for Resource in db:
        resource = Resource()
        for route in wrap(Resource.routes):
            api.add_route(route, resource)
            spec.path(resource=resource)
            log.success(f'{route} endpoint configured')

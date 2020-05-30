from resource.agent.catalog import AgentCatalogResource
from resource.agent.catalog.selected import AgentCatalogSelectedResource

from resource.agent.instance import AgentInstanceResource
from resource.agent.instance.selected import AgentInstanceSelectedResource

from resource.connection import ConnectionResource
from resource.connection.selected import ConnectionSelectedResource

from resource.data import DataResource
from resource.data.selected import DataSelectedResource

from resource.ebpf_program.catalog import eBPFProgramCatalogResource
from resource.ebpf_program.catalog.selected import eBPFProgramCatalogSelectedResource

from resource.ebpf_program.instance import eBPFProgramInstanceResource
from resource.ebpf_program.instance.selected import eBPFProgramInstanceSelectedResource

from resource.exec_env import ExecEnvResource
from resource.exec_env.selected import ExecEnvSelectedResource

from resource.exec_env.type import ExecEnvTypeResource
from resource.exec_env.type.selected import ExecEnvTypeSelectedResource

from resource.network_link import NetworkLinkResource
from resource.network_link.selected import NetworkLinkSelectedResource

from resource.network_link.type import NetworkLinkTypeResource
from resource.network_link.type.selected import NetworkLinkTypeSelectedResource

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

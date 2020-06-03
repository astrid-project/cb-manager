from document.agent.catalog import AgentCatalogDocument
from document.exec_env import ExecEnvDocument
from resource.agent.handler.lcp.execute import actions, parameters
from resource.base.handler.lcp.retrieve import from_doc


def lcp_post(instance, req, resp):
    resp['lcp'] = resp_lcp = []
    resp_data = resp.get('data')

    agent_catalog = from_doc(document=AgentCatalogDocument, id=resp_data.get('agent_catalog_id', None),
                             name='Agent Catalog', resp_lcp=resp_lcp)
    exec_env = from_doc(document=ExecEnvDocument, id=resp_data.get('exec_env_id', None),
                        name='Execution Environment', resp_lcp=resp_lcp)

    if all([agent_catalog, exec_env]):
        actions(instance=instance, catalog=agent_catalog.actions, data=req.get('actions', []),
                exec_env=exec_env, resp_lcp=resp_lcp)
        parameters(instance=instance, catalog=agent_catalog.parameters, data=req.get('parameters', []),
                   exec_env=exec_env, resp_lcp=resp_lcp)

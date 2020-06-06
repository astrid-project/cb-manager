from elasticsearch_dsl import Document, InnerDoc, Nested, Text


class AgentInstanceParameterInnerDoc(InnerDoc):
    """Parameter of the agent instance installed in an execution environment."""
    id = Text(required=True)
    value = Text(required=True)


class AgentInstanceDocument(Document):
    """Represents an agent instance installed in an execution environment."""
    # id already defined by Elasticsearch
    agent_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)
    status = Text(required=True)
    parameters = Nested(AgentInstanceParameterInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'agent-instance'

from elasticsearch_dsl import Boolean, Document, InnerDoc, Nested, Text


class AgentCatalogParameterConfigInnerDoc(InnerDoc):
    """Agent parameter configuration."""
    schema = Text(required=True)
    source = Text(required=True)
    path = Text(required=True)


class AgentCatalogParameterInnerDoc(InnerDoc):
    """Agent parameter."""
    id = Text(required=True)
    type = Text(required=True) # possible values: integer, number, time-duration, string, choice, boolean, binary
    config = Nested(AgentCatalogParameterConfigInnerDoc, required=True)
    list = Boolean()
    values = Text() # when type = choice
    description = Text()
    example = Text()


class AgentCatalogActionConfigInnerDoc(InnerDoc):
    """Agent action configuration."""
    cmd = Text(required=True)
    args = Text()
    daemon = Text()


class AgentCatalogActionInnerDoc(InnerDoc):
    """Agent action."""
    config = Nested(AgentCatalogActionConfigInnerDoc, required=True)
    status = Text()
    description = Text()


class AgentCatalogDocument(Document):
    """Represents an agent in the catalog."""
    # id already defined by Elasticsearch
    actions = Nested(AgentCatalogActionInnerDoc)
    parameters = Nested(AgentCatalogParameterInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'agent-catalog'

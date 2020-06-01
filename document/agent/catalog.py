from elasticsearch_dsl import Boolean, Document, InnerDoc, Nested, Text


class AgentCatalogParameterConfigInnerDoc(InnerDoc):
    """Agent parameter configuration."""
    #FIXME description?
    schema = Text(required=True)
    source = Text(required=True)
    path = Text(required=True)


class AgentCatalogParameterInnerDoc(InnerDoc):
    """Agent parameter."""
    id = Text(required=True)
    description = Text()
    type = Text(required=True) # possible values: integer, number, time-duration, string, choice, boolean, binary
    list = Boolean()
    values = Text() # when type = choice
    example = Text()
    config = Nested(AgentCatalogParameterConfigInnerDoc, required=True)


class AgentCatalogActionConfigInnerDoc(InnerDoc):
    """Agent action configuration."""
    description = Text()
    cmd = Text(required=True)


class AgentCatalogActionInnerDoc(InnerDoc):
    """Agent action."""
    description = Text()
    config = Nested(AgentCatalogActionConfigInnerDoc, required=True)


class AgentCatalogDocument(Document):
    """Represents an agent in the catalog."""
    # id already defined by Elasticsearch
    description = Text()
    parameters = Nested(AgentCatalogParameterInnerDoc, required=True)
    actions = Nested(AgentCatalogActionInnerDoc, required=True)

    class Index:
        """Elasticsearch configuration."""
        name = 'agent-catalog'

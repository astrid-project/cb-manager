from elasticsearch_dsl import Boolean, Document, InnerDoc, Nested, Text


class AgentCatalogParameterConfigInnerDoc(InnerDoc):
    """
    Agent parameter configuration.
    """
    schema = Text(required=True)
    source = Text(required=True)
    path = Text(required=True)


class AgentCatalogParameterInnerDoc(InnerDoc):
    """
    Agent parameter.
    """
    id = Text(required=True)
    # Possible values: integer, number, time-duration, string, choice, boolean, binary
    type = Text(required=True)
    list = Boolean()
    values = Text() # when type = choice
    example = Text()
    description = Text()
    config = Nested(AgentCatalogParameterConfigInnerDoc, required=True)


class AgentCatalogActionConfigInnerDoc(InnerDoc):
    """
    Agent action configuration.
    """
    description = Text()
    cmd = Text(required=True)


class AgentCatalogActionInnerDoc(InnerDoc):
    """
    Agent action.
    """
    description = Text()
    config = Nested(AgentCatalogActionConfigInnerDoc, required=True)


class AgentCatalogDocument(Document):
    """
    Represents an agent in the catalog.
    """
    # id already defined by Elasticsearch
    parameters = Nested(AgentCatalogParameterInnerDoc, required=True)
    actions = Nested(AgentCatalogActionInnerDoc, required=True)
    description = Text()

    class Index:
        # TODO add docstring.
        name = 'agent-catalog'

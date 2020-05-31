from elasticsearch_dsl import Document, Text


class NetworkLinkTypeDocument(Document):
    """
    Represents a network link type.
    """

    # id already defined by Elasticsearch

    name = Text(required=True)

    description = Text()

    class Index:
        name = 'network-link-type'

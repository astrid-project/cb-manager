from elasticsearch_dsl import Document, Text


class NetworkLinkDocument(Document):
    """
    Represents a network link.
    """

    # id already defined by Elasticsearch

    type_id = Text(required=True)

    class Index:
        name = 'network-link'

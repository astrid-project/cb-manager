from elasticsearch_dsl import Document, Text


class ExecEnvTypeDocument(Document):
    # id already defined by Elasticsearch

    name = Text(required=True)

    description = Text()

    class Index:
        name = 'exec-env-type'

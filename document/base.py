from elasticsearch_dsl import Document


class BaseDocument(Document):
    @classmethod
    def get_ids(cls):
        s = cls.search()
        return [doc.meta.id for doc in s.execute()]


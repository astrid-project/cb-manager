from elasticsearch_dsl import Document
from script import read as script_read


class BaseDocument(Document):
    @classmethod
    def get_ids(cls):
        s = cls.search()
        return [doc.meta.id for doc in s.execute()]

    def edit(self, data, field, def_op='edit'):
        return self.__update(data=self.__filter(data, op='edit'), op='edit', field=field)

    def rm(self, data, field, def_op='edit'):
        return self.__update(data=list(map(lambda d: d['id'], self.__filter(data, op='rm'))),
                             op='rm', field=field)

    @staticmethod
    def __filter(data, op, def_op='edit'):
        return list(filter(lambda d: d.get('__op', def_op) == op, data))

    def __update(self, data, op, field):
        if len(data) > 0:
            return self.update(script=script_read(f'nested_field/{op}.pl', nested_field=field), data=data)
        else:
            return 'noop'

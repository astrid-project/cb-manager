from reader.arg import ArgReader
from time import sleep
from utils.log import Log


class BaseResource(object):
    tag = []
    doc_cls = None
    lcp_handler = {}
    nested_fields = []
    readonly_fields = []
    ignore_fields = []

    def __init__(self):
        if self.doc_cls is not None:
            self.log = Log.get(self.doc_cls.Index.name)
            error_es_initialization = True
            while error_es_initialization:
                try:
                    self.log.info(f'start initialization index {self.doc_cls.Index.name}')
                    self.doc_cls.init()
                except Exception as exception:
                    self.log.error(f'Exception: {exception}')
                    self.log.error(f'initialization index {self.doc_cls.Index.name} not possible')
                    self.log.info(f'waiting for {ArgReader.db.es_retry_period} seconds and try again')
                    sleep(ArgReader.db.es_retry_period)
                    self.__init__()
                else:
                    self.log.success(f'index {self.doc_cls.Index.name} initialized')
                    error_es_initialization = False
        else:
            Log.get(self.__class__.__name__).warning('doc_cls not set')

    from resource.base.get import on_base_get
    from resource.base.post import on_base_post
    from resource.base.put import on_base_put
    from resource.base.delete import on_base_delete

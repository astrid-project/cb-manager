
class BaseResource(object):
    def __init_(self, document_class):
        self.doc_cls = document_class

    def on_get(self, req, resp):
        try:
            res = QueryParser(index=self.doc.Index.name).parse(
                query=req.context['json']).execute()
            resp.media = [dict(item.to_dict(), id=item.meta.id) for item in res]
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(title=req_error.error(), description=req_error.info())

    def on_post(self, req, resp):
        data = req.context['json']
        id = data.pop('id', None)
        if id is None:
            raise falcon.HTTPBadRequest(title='Request not valid', description='id property not found')
        try:
            self.doc?class.get(id=id)
        except elasticsearch.NotFoundError:
            resp.media = ExecEnvDocument(
                meta={'id': id}, **data).save().to_dict()
        else:
            raise falcon.HTTPConflict(title='Execution Environment already found', description=f'id={id} already present')

    def on_delete(self, req, resp):
        try:
            resp.media = QueryParser(index=ExecEnvDocument.Index.name).parse(
                query=req.context['json']).delete().to_dict()
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(title=req_error.error(), description=req_error.info())

    def on_put(self, req, resp):
        data = req.context['json']
        id = data.pop('id', None)
        if id is None:
            raise falcon.HTTPBadRequest(title='Request not valid', description='id property not found')
        try:
            resp.media = ExecEnvDocument.get(id=id).update(**data).to_dict()
        except elasticsearch.NotFoundError:
            raise falcon.HTTPNotFound(title=f'Execution Environment not found',
                                      description='Execution Environment with id = {id} not found')

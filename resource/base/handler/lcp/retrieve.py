from http import HTTPStatus
from utils.log import Log


def from_doc(document, id, name, resp_lcp):
    try:
        return document.get(id=id)
    except Exception as exception:
        Log.get('lcp').error(f'Exception: {exception}')
        resp_lcp.append(dict(status='error', error=True, description=f'{name} {id} unknown.',
                             exception=str(exception), http_status_code=HTTPStatus.NOT_FOUND))
        return None


def from_catalog(catalog, id, type, label, resp_lcp):
    ret = list(filter(lambda x: x.id == id, catalog))
    if len(ret) == 1:
        return ret[0]
    else:
        resp_lcp.append(dict(status='error', error=True, description=f'{label.title()} {id} unknown.',
                             data=dict(type=type), http_status_code=HTTPStatus.NOT_FOUND))
        return None

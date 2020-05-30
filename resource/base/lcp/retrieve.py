from http import HTTPStatus
from utils.log import Log


def from_doc(document, id, name, resp_lcp):
    log = Log.get('lcp')
    try:
        return document.get(id=id)
    except Exception as exception:
        log.error(f'Exception: {exception}')
        resp_lcp.append(dict(status='error',
                             reason=f'{name} {id} unknown.',
                             http_status_code=HTTPStatus.NOT_FOUND))
        return None


def from_catalog(catalog, id, type, label, resp_lcp):
    ret = list(filter(lambda x: x.id == id, catalog))
    if len(ret) == 1:
        return ret[0]
    else:
        result.append(dict(type=type,
                           status='error',
                           reason=f'{label.title()} {id} unknown.',
                           http_status_code=HTTPStatus.NOT_FOUND))
        return None

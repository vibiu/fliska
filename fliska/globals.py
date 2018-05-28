from functools import partial

from werkzeug.local import LocalStack, LocalProxy

_request_ctx_err_msg = '''\
Working outside of request context.\
'''


_app_ctx_err_msg = '''\
Working outside of app context.\
'''


def _lookup_req_object(name):
    top = _request_ctx_stack.top

    if top is None:
        raise RuntimeError(_request_ctx_err_msg)
    return getattr(top, name)


def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return getattr(top, name)


_request_ctx_stack = LocalStack()
_app_ctx_stack = LocalStack()

request = LocalProxy(partial(_lookup_req_object, 'body'))
g = LocalProxy(partial(_lookup_req_object, 'g'))

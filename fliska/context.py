from .globals import _request_ctx_stack, _app_ctx_stack


class AppContext:

    def __init__(self, app):
        self.app = app

    def push(self):
        _app_ctx_stack.push(self)

    def pop(self):
        _app_ctx_stack.pop()

    def __enter__(self):
        self.push()
        return self

    def __exit__(self):
        self.pop()


class RequestContext:

    def __init__(self, app, body, request=None):
        self.app = app

        # if request is None:
        #     request = app.request_class(environ)
        self.request = request
        self.body = body

        self._implicit_app_ctx_stack = []
        self.preserved = False

    def push(self):
        app_ctx = _app_ctx_stack.top
        if app_ctx is None or app_ctx.app != self.app:
            app_ctx = self.app.app_context()
            app_ctx.push()
        _request_ctx_stack.push(self)

    def pop(self):
        _request_ctx_stack.pop()

    def auto_pop(self):
        self.pop()

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.auto_pop()

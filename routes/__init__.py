class Route(object):

    routes = {}

    def __init__(self):
        pass
    @classmethod
    def resolveMethod(cls, method):
        return tuple(map(
            lambda x: x.strip(),
            method.strip().split('@')
        ))

    @classmethod
    def get(cls, path, method):
        controller, method = cls.resolveMethod(method)
        cls.routes.setdefault(controller, {})
        cls.routes[controller].setdefault(method, [path, 'get'])

from routes import web
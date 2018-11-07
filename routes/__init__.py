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
    def bindHttpMethod(cls, httpMethod, path, method):
        controller, method = cls.resolveMethod(method)
        if controller not in cls.routes:
            cls.routes.setdefault(controller, {})
        cls.routes[controller].setdefault(method, [path, httpMethod])

    @classmethod
    def get(cls, path, method):
        cls.bindHttpMethod('GET', path, method)
    
    @classmethod
    def post(cls, path, method):
        cls.bindHttpMethod('POST', path, method)
    
    @classmethod
    def put(cls, path, method):
        cls.bindHttpMethod('PUT', path, method)
    
    @classmethod
    def delete(cls, path, method):
        cls.bindHttpMethod('DELETE', path, method)

from routes import web
import importlib
from flask import Flask, app, render_template, url_for, _request_ctx_stack
from routes import Route

class Application(Flask):
    def __init__(
        self,
        import_name
    ):
        super(Application, self).__init__(
            import_name,
            '/public',
            'public'
        )
        self.build()
        self.register()

    @classmethod
    def initFuns(cls):
        cls.funs = {}
    
    @classmethod
    def embellish(cls, fun):
        cls.funs[fun.__name__] = fun

    def build(self):
        self.routes = Route.routes
        for controller, routesDict in Route.routes.items():
            self.initFuns()
            importlib.import_module('.' + controller, 'app.Controllers')
            for funName, fun in self.funs.items():
                self.funName = controller[0:-10].lower() + funName.capitalize()
                self.route(routesDict[funName][0], methods=[routesDict[funName][1]])(fun)
            
    def register(self):
        self.registerViewMethod()
        self.registerUrlFor()
        self.registerStatic()
        self.registerBootstrap()

    @app.setupmethod
    def add_url_rule(self, rule, endpoint=None, view_func=None,
                     provide_automatic_options=None, **options):
        """Connects a URL rule.  Works exactly like the :meth:`route`
        decorator.  If a view_func is provided it will be registered with the
        endpoint.

        Basically this example::

            @app.route('/')
            def index():
                pass

        Is equivalent to the following::

            def index():
                pass
            app.add_url_rule('/', 'index', index)

        If the view_func is not provided you will need to connect the endpoint
        to a view function like so::

            app.view_functions['index'] = index

        Internally :meth:`route` invokes :meth:`add_url_rule` so if you want
        to customize the behavior via subclassing you only need to change
        this method.

        For more information refer to :ref:`url-route-registrations`.

        .. versionchanged:: 0.2
           `view_func` parameter added.

        .. versionchanged:: 0.6
           ``OPTIONS`` is added automatically as method.

        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param view_func: the function to call when serving a request to the
                          provided endpoint
        :param provide_automatic_options: controls whether the ``OPTIONS``
            method should be added automatically. This can also be controlled
            by setting the ``view_func.provide_automatic_options = False``
            before adding the rule.
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.  A change
                        to Werkzeug is handling of method options.  methods
                        is a list of methods this rule should be limited
                        to (``GET``, ``POST`` etc.).  By default a rule
                        just listens for ``GET`` (and implicitly ``HEAD``).
                        Starting with Flask 0.6, ``OPTIONS`` is implicitly
                        added and handled by the standard request handling.
        """
        if endpoint is None:
            endpoint = self.funName
        options['endpoint'] = endpoint
        methods = options.pop('methods', None)

        # if the methods are not given and the view_func object knows its
        # methods we can use that instead.  If neither exists, we go with
        # a tuple of only ``GET`` as default.
        if methods is None:
            methods = getattr(view_func, 'methods', None) or ('GET',)
        if isinstance(methods, app.string_types):
            raise TypeError('Allowed methods have to be iterables of strings, '
                            'for example: @app.route(..., methods=["POST"])')
        methods = set(item.upper() for item in methods)

        # Methods that should always be added
        required_methods = set(getattr(view_func, 'required_methods', ()))

        # starting with Flask 0.8 the view_func object can disable and
        # force-enable the automatic options handling.
        if provide_automatic_options is None:
            provide_automatic_options = getattr(view_func,
                                                'provide_automatic_options', None)

        if provide_automatic_options is None:
            if 'OPTIONS' not in methods:
                provide_automatic_options = True
                required_methods.add('OPTIONS')
            else:
                provide_automatic_options = False

        # Add the required methods now.
        methods |= required_methods

        rule = self.url_rule_class(rule, methods=methods, **options)
        rule.provide_automatic_options = provide_automatic_options

        self.url_map.add(rule)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: %s' % endpoint)
            self.view_functions[endpoint] = view_func
            
    def dispatch_request(self):
        """Does the request dispatching.  Matches the URL and returns the
        return value of the view or error handler.  This does not have to
        be a response object.  In order to convert the return value to a
        proper response object, call :func:`make_response`.

        .. versionchanged:: 0.7
           This no longer does the exception handling, this code was
           moved to the new :meth:`full_dispatch_request`.
        """
        req = _request_ctx_stack.top.request
        if req.routing_exception is not None:
            self.raise_routing_exception(req)
        rule = req.url_rule
        # if we provide automatic options for this URL and the
        # request came with the OPTIONS method, reply automatically
        if getattr(rule, 'provide_automatic_options', False) \
           and req.method == 'OPTIONS':
            return self.make_default_options_response()
        # otherwise dispatch to the handler for that endpoint
        print(str(req.view_args))
        return self.view_functions[rule.endpoint](self, **req.view_args)

    def registerViewMethod(self):
        def view(template, **options):
            return render_template(
                template + '.html',
                app=self,
                **options
            )
        self.view = view
    
    def registerUrlFor(self):
        self.url = url_for
        
    def registerStatic(self):
        def static(path):
            return self.static_url_path + path
        self.static = static
       
    def registerBootstrap(self):
        def bootstrap(file):
            return self.static('/bootstrap/dist') + file
        self.bootstrap = bootstrap
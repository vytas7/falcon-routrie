import threading
import typing

import falcon.routing
import routrie


class RoutrieRouter:
    def __init__(self):
        self._lock = threading.Lock()
        self._routes = {}
        self._router = None

        self.find = self._compile_and_find

    def add_route(
        self,
        uri_template: str,
        resource: object,
        suffix: typing.Optional[str] = None,
        **kwargs
    ):
        # if uri_template in self._routes:
        # TODO: then raise?

        self._routes[uri_template] = (
            resource,
            falcon.routing.map_http_methods(resource, suffix=suffix),
            uri_template,
        )

        self.find = self._compile_and_find

    def _compile_and_find(self, uri: str, req: object = None):
        with self._lock:
            self._router = routrie.Router(self._routes)
            self.find = self._find

            return self._find(uri, req=req)

    def _find(self, uri: str, req: object = None):
        found = self._router.find(uri)
        if found is not None:
            (resource, method_map, uri_template), params = found
            return resource, method_map, params, uri_template

        return None

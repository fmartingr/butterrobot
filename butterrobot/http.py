class ExternalProxyFix(object):
    """
    Custom proxy helper to get the external hostname from the `X-External-Host` header
    used by one of the reverse proxies in front of this in production.
    It does nothing if the header is not present.
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        host = environ.get("HTTP_X_EXTERNAL_HOST", "")
        if host:
            environ["HTTP_HOST"] = host
        return self.app(environ, start_response)

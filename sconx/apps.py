from connexion import FlaskApp
from sconx.compression import CompressionAppMixin
from sconx.jsan import JSANAPI


class App(FlaskApp):
    def __init__(self, import_name, *args, **kwargs):
        super(FlaskApp, self).__init__(import_name, JSANAPI, *args, **kwargs)


class TextCompressionApp(FlaskApp, CompressionAppMixin):
    def __init__(self, *args, compress=None, decompress=None, **kwargs):
        super().__init__(*args, **kwargs)
        CompressionAppMixin.__init__(self, compress, decompress)


class CompressionApp(App, CompressionAppMixin):
    def __init__(self, *args, compress=None, decompress=None, **kwargs):
        super().__init__(*args, **kwargs)
        CompressionAppMixin.__init__(self, compress, decompress)

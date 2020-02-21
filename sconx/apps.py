from connexion import FlaskApp
from sconx.jsan import JSANAPI


class App(FlaskApp):
    def __init__(self, import_name, *args, **kwargs):
        super(FlaskApp, self).__init__(import_name, JSANAPI, *args, **kwargs)

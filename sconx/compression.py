import io

from connexion.apps.flask_app import FlaskJSONEncoder


class MinifiedJSONEncoder(FlaskJSONEncoder):
    item_separator = ","
    key_separator = ":"


class CompressionAppMixin:
    def __init__(self, compress=None, decompress=None):
        self.compress = compress
        if decompress:
            self.app.wsgi_app = DecompressionMiddleware(self.app.wsgi_app, decompress)
        if compress:
            self.app.after_request(self.after_request)

        self.app.json_encoder = MinifiedJSONEncoder

    def after_request(self, response):
        """
        set_data seems more explicit than using iterable directly in middleware
        XXX: Maybe custom Response?
        """
        if response.content_encoding:
            algs = get_compression_algs(self.compress, response.content_encoding)
            response.set_data(apply_compression(algs, response.data.decode()))
        return response


def apply_compression(algs, text):
    for alg in algs:
        text = alg(text)
    return text


def decompress_bytes(body, length, encodings):
    decompressed = body.read(length).decode()
    for alg in encodings:
        decompressed = alg(decompressed)
    return decompressed


def separate_alg_names(encoding):
    return [] if encoding == "" else encoding.split(",")


def get_compression_algs(algs_mapping, encoding_header):
    alg_names = map(str.strip, separate_alg_names(encoding_header))
    return map(lambda name: algs_mapping[name], alg_names)


def get_decompression_algs(*args, **kwargs):
    return reversed(list(get_compression_algs(*args, **kwargs)))


class DecompressionMiddleware:
    """
    flask requests shall be immutable so decompression is done on wsgi level
    XXX: Maybe custom Request?
    """

    def __init__(self, app, decompress):
        self.app = app
        self.decompress = decompress

    def __call__(self, environ, start_response):
        algs = get_decompression_algs(
            self.decompress, environ.get("HTTP_CONTENT_ENCODING", "")
        )
        body = decompress_bytes(
            environ["wsgi.input"], int(environ.get("CONTENT_LENGTH", 0)), algs
        )

        environ["wsgi.input"] = io.BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = len(body)
        res = self.app(environ, start_response)

        return res

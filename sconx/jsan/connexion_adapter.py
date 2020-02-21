import flask
from connexion import FlaskApi, FlaskApp, operations, request, spec
from sconx.jsan.from_jsan import from_jsan
from sconx.jsan.to_jsan import to_jsan

JSAN_CONTENT_TYPE = "application/jsan"
is_jsan = lambda request: request.headers.get("Content-Type") == JSAN_CONTENT_TYPE


class JSANOperation(operations.OpenAPIOperation):
    def _get_body_argument(self, body, arguments, has_kwargs, sanitize):
        x_body_name = sanitize(self.body_schema.get("x-body-name", "body"))

        if is_jsan(request) and JSAN_CONTENT_TYPE in self.consumes:
            return {
                x_body_name: from_jsan(self.body_schema, request.get_json(force=True))
            }

        return super()._get_body_argument(body, arguments, has_kwargs, sanitize)


class JSANSpecification(spec.OpenAPISpecification):
    operation_cls = JSANOperation


class Specification(spec.Specification):
    @classmethod
    def from_dict(cls, spec):
        """
        Copied from connexion connexion.spec.Specification just to replace OpenAPISpecification
        """

        def enforce_string_keys(obj):
            # YAML supports integer keys, but JSON does not
            if isinstance(obj, dict):
                return {str(k): enforce_string_keys(v) for k, v in obj.items()}
            return obj

        spec = enforce_string_keys(spec)
        version = cls._get_spec_version(spec)
        if version < (3, 0, 0):
            return Swagger2Specification(spec)

        # OpenAPISpecification swapped with CompressableSpecification - the only thing changed in this method.
        return JSANSpecification(spec)


class JSANAPI(FlaskApi):
    @classmethod
    def _serialize_data(cls, data, mimetype):
        if mimetype == JSAN_CONTENT_TYPE:
            data = cls.jsonifier.dumps(to_jsan(data))
        return super(JSANAPI, cls)._serialize_data(data, mimetype)

    def __init__(
        self,
        specification,
        base_path=None,
        arguments=None,
        validate_responses=False,
        strict_validation=False,
        resolver=None,
        auth_all_paths=False,
        debug=False,
        resolver_error_handler=None,
        validator_map=None,
        pythonic_params=False,
        pass_context_arg_name=None,
        options=None,
    ):
        """
        Copied connexion.apis.abstract.AbstractAPI.__init__ + added necessary imports. Done just to use custom Specification class
        """
        import logging

        logger = logging.getLogger("connexion.apis.flask_api")
        from connexion.options import ConnexionOptions
        from connexion.resolver import Resolver

        self.debug = debug
        self.validator_map = validator_map
        self.resolver_error_handler = resolver_error_handler

        logger.debug(
            "Loading specification: %s",
            specification,
            extra={
                "swagger_yaml": specification,
                "base_path": base_path,
                "arguments": arguments,
                "auth_all_paths": auth_all_paths,
            },
        )

        # Avoid validator having ability to modify specification
        self.specification = Specification.load(specification, arguments=arguments)

        logger.debug("Read specification", extra={"spec": self.specification})

        self.options = ConnexionOptions(options, oas_version=self.specification.version)

        logger.debug(
            "Options Loaded",
            extra={
                "swagger_ui": self.options.openapi_console_ui_available,
                "swagger_path": self.options.openapi_console_ui_from_dir,
                "swagger_url": self.options.openapi_console_ui_path,
            },
        )

        self._set_base_path(base_path)

        logger.debug(
            "Security Definitions: %s", self.specification.security_definitions
        )

        self.resolver = resolver or Resolver()

        logger.debug("Validate Responses: %s", str(validate_responses))
        self.validate_responses = validate_responses

        logger.debug("Strict Request Validation: %s", str(strict_validation))
        self.strict_validation = strict_validation

        logger.debug("Pythonic params: %s", str(pythonic_params))
        self.pythonic_params = pythonic_params

        logger.debug("pass_context_arg_name: %s", pass_context_arg_name)
        self.pass_context_arg_name = pass_context_arg_name

        if self.options.openapi_spec_available:
            self.add_openapi_json()
            self.add_openapi_yaml()

        if self.options.openapi_console_ui_available:
            self.add_swagger_ui()

        self.add_paths()

        if auth_all_paths:
            self.add_auth_on_not_found(
                self.specification.security, self.specification.security_definitions
            )

    @classmethod
    def _set_jsonifier(cls):
        """ By default connexion renders json with indent=2 """
        cls.jsonifier = flask.json

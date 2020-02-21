import random

import pytest


@pytest.fixture
def primitive():
    return random.random()


@pytest.fixture
def primitive_spec():
    return {"type": "number"}


@pytest.fixture
def dict_json():
    return {"c": 1, "b": "string", "a": 2}


@pytest.fixture
def dict_jsan():
    return [2, "string", 1]


@pytest.fixture
def dict_spec():
    return {
        "type": "object",
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "string"},
            "c": {"type": "integer"},
        },
    }


@pytest.fixture
def array_json(dict_json):
    return [dict_json, {"b": "nextstr", "a": 8, "c": 3}]


@pytest.fixture
def array_jsan(dict_jsan):
    return [dict_jsan, [8, "nextstr", 3]]


@pytest.fixture
def array_spec(dict_spec):
    return {"type": "array", "items": dict_spec}


@pytest.fixture
def nested_json(dict_json, array_json):
    return {"dict": dict_json, "array": array_json}


@pytest.fixture
def nested_jsan(dict_jsan, array_jsan):
    return [array_jsan, dict_jsan]


@pytest.fixture
def nested_spec(dict_spec, array_spec):
    return {"type": "object", "properties": {"dict": dict_spec, "array": array_spec}}

import pytest
from sconx.jsan import from_jsan, to_jsan


def test_primitives_stay_unchanged(primitive_spec, primitive):
    assert to_jsan(primitive) == primitive
    assert from_jsan(primitive_spec, primitive) == primitive


def test_array_to_jsan(array_json, array_jsan):
    assert to_jsan(array_json) == array_jsan


def test_array_from_jsan(array_spec, array_json, array_jsan):
    assert list(from_jsan(array_spec, array_jsan)) == array_json


def test_nested_to_jsan(nested_json, nested_jsan):
    assert to_jsan(nested_json) == nested_jsan


def test_nested_from_jsan(nested_spec, nested_json, nested_jsan):
    result = from_jsan(nested_spec, nested_jsan)
    result["array"] = list(result["array"])
    assert result == nested_json


@pytest.fixture
def mixed_type_array_spec():
    return {"type": "array", "items": {"oneOf": ["string", "integer"]}}


@pytest.fixture
def nested_array_spec(mixed_type_array_spec):
    return {"type": "array", "items": mixed_type_array_spec}


def test_array_of_primitives_stay_unchanged(mixed_type_array_spec, dict_jsan):
    assert to_jsan(dict_jsan) == dict_jsan
    assert list(from_jsan(mixed_type_array_spec, dict_jsan)) == dict_jsan


def test_array_of_arrays_stay_unchanged(nested_array_spec, array_jsan):
    assert to_jsan(array_jsan) == array_jsan
    assert list(map(list, from_jsan(nested_array_spec, array_jsan))) == array_jsan

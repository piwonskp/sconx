import json

import pytest
import sconx

app = sconx.App(__name__)
app.add_api("api.yml")


@pytest.fixture(scope="module")
def client():
    with app.app.test_client() as c:
        yield c


@pytest.fixture
def expected_response():
    return [3, "string", 1]


def test_connexion_integration(client, dict_jsan, expected_response):
    response = client.post(
        "/test-route",
        data=json.dumps(dict_jsan),
        headers={"Content-Type": "application/jsan"},
    )
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == expected_response

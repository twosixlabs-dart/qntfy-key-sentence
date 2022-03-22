import json

import pytest
from falcon import testing

from ceeder import cdr, validate
from analytic import create, LABEL


@pytest.fixture()
def client():
    return testing.TestClient(create())


def test_get_message(client):
    sample_cdr = cdr(extracted_text="Hello world!!!")

    # perform a POST request, as one would in CURL
    result = client.simulate_post("/api/v1/annotate/cdr", json=sample_cdr)
    output = result.json
    assert output["label"] == LABEL
    assert output["type"] == "tags"
    sample_cdr["annotators"] = output
    validate(sample_cdr)

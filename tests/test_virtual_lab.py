from flask.testing import FlaskClient
from requests import get, post, put
from requests.auth import HTTPBasicAuth

from portl.functions import fetch_all

from tests.test_base import check_blueprints


@check_blueprints("/inventory")
def test_rest_api_basic(user_client: FlaskClient) -> None:
    assert len(fetch_all("Device")) == 28
    post(
        "http://192.168.105.2:5000/rest/instance/device",
        json={"name": "new_router", "model": "Cisco"},
        auth=HTTPBasicAuth("admin", "admin"),
    )
    # assert len(fetch_all("Device")) == 29
    result = get(
        "http://192.168.105.2:5000/rest/instance/device/Washington",
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["model"] == "Arista" and len(result) == 21
    post(
        "http://192.168.105.2:5000/rest/instance/device",
        json={"name": "Washington", "model": "Cisco"},
        auth=HTTPBasicAuth("admin", "admin"),
    )
    result = get(
        "http://192.168.105.2:5000/rest/instance/device/Washington",
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["model"] == "Cisco" and len(result) == 21
    result = get(
        "http://192.168.105.2:5000/rest/instance/service/get_facts",
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["description"] == "Getter: get_facts" and len(result) == 39
    put(
        "http://192.168.105.2:5000/rest/instance/service",
        json={"name": "get_facts", "description": "Get facts"},
        auth=HTTPBasicAuth("admin", "admin"),
    )
    result = get(
        "http://192.168.105.2:5000/rest/instance/service/get_facts",
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["description"] == "Getter: get_facts" and len(result) == 39
    assert len(fetch_all("Service")) == 25
    result = post(
        "http://192.168.105.2:5000/rest/instance/service",
        json={"name": "new_service", "vendor": "Cisco"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["vendor"] == "Cisco" and len(fetch_all("Service")) == 26
    assert len(fetch_all("Workflow")) == 5
    result = post(
        "http://192.168.105.2:5000/rest/instance/workflow",
        json={"name": "new_workflow", "description": "New"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["description"] == "New" and len(fetch_all("Workflow")) == 6


@check_blueprints("/automation")
def test_payload_transfer_workflow(user_client: FlaskClient) -> None:
    result = post(
        "http://192.168.105.2:5000/rest/run_job",
        json={"name": "payload_transfer_workflow"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["results"]["success"] and len(result) == 2
    post(
        "http://192.168.105.2:5000/rest/instance/Workflow",
        json={"name": "payload_transfer_workflow", "multiprocessing": True},
        auth=HTTPBasicAuth("admin", "admin"),
    )
    result = post(
        "http://192.168.105.2:5000/rest/run_job",
        json={"name": "payload_transfer_workflow"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["results"]["success"] and len(result) == 2


@check_blueprints("/automation")
def test_netmiko_workflow(user_client: FlaskClient) -> None:
    result = post(
        "http://192.168.105.2:5000/rest/run_job",
        json={"name": "Netmiko_VRF_workflow"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["results"]["success"] and len(result) == 2
    post(
        "http://192.168.105.2:5000/rest/instance/Workflow",
        json={"name": "Netmiko_VRF_workflow", "multiprocessing": True},
        auth=HTTPBasicAuth("admin", "admin"),
    )
    result = post(
        "http://192.168.105.2:5000/rest/run_job",
        json={"name": "Netmiko_VRF_workflow"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["results"]["success"] and len(result) == 2
    post(
        "http://192.168.105.2:5000/rest/instance/Workflow",
        json={"name": "Netmiko_VRF_workflow", "use_workflow_targets": False},
        auth=HTTPBasicAuth("admin", "admin"),
    )
    result = post(
        "http://192.168.105.2:5000/rest/run_job",
        json={"name": "Netmiko_VRF_workflow"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["results"]["success"] and len(result) == 2


@check_blueprints("/automation")
def test_napalm_workflow(user_client: FlaskClient) -> None:
    result = post(
        "http://192.168.105.2:5000/rest/run_job",
        json={"name": "Napalm_VRF_workflow"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["results"]["success"] and len(result) == 2
    post(
        "http://192.168.105.2:5000/rest/instance/Workflow",
        json={"name": "Napalm_VRF_workflow", "multiprocessing": True},
        auth=HTTPBasicAuth("admin", "admin"),
    )
    result = post(
        "http://192.168.105.2:5000/rest/run_job",
        json={"name": "Napalm_VRF_workflow"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["results"]["success"] and len(result) == 2
    post(
        "http://192.168.105.2:5000/rest/instance/Workflow",
        json={"name": "Napalm_VRF_workflow", "use_workflow_targets": False},
        auth=HTTPBasicAuth("admin", "admin"),
    )
    result = post(
        "http://192.168.105.2:5000/rest/run_job",
        json={"name": "Napalm_VRF_workflow"},
        auth=HTTPBasicAuth("admin", "admin"),
    ).json()
    assert result["results"]["success"] and len(result) == 2

import json
import pytest
import sys
from requests import Request, Session

session = Session()
address = "http://127.0.0.1:8002/"

# path building variables
RESOURCES_PATH = "../../resources/"
IMAGES_PATH = "images/"
OUTPUT_PATH = "output/"

# local paths
LOCAL_IMAGES_PATH = RESOURCES_PATH + IMAGES_PATH
LOCAL_OUTPUT_PATH = RESOURCES_PATH + OUTPUT_PATH


@pytest.fixture()
def json_edit_image() -> json:
    data = json.loads('{}')
    data["images_paths"] = ["1.jpeg", "2.jpeg"]
    return data


@pytest.fixture()
def memory_header() -> json:
    headers = json.loads('{}')
    headers["Memory-Test"] = "True"
    return headers


def print_PATCH(req):
    print('\n{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------REQ-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body
    ))


def print_PATCH_resp(resp):
    print('\n{}\n{}\n{}'.format(
        '-----------RESP-----------',
        resp.status_code,
        resp.content
    ))


def test_patch_flip_horziontal_ok(json_edit_image, memory_header):
    url = address + "flip-horizontal"
    req_json = json_edit_image
    req_headers = memory_header

    req = Request('PATCH', url, json=req_json, headers=req_headers)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    assert response.status_code == 200

    output1 = open("memory_delta/flip_horziontal.txt", "a")
    output2 = open("memory_max/flip_horziontal.txt", "a")
    output1.write(response.headers["memory_spike"] + " ")
    output1.close()
    output2.write(response.headers["memory_peak"] + " ")
    output2.close()


def test_patch_flip_vertical_ok(json_edit_image, memory_header):
    url = address + "flip-vertical"
    req_json = json_edit_image
    req_headers = memory_header

    req = Request('PATCH', url, json=req_json, headers=req_headers)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    assert response.status_code == 200

    output1 = open("memory_delta/flip_vertical.txt", "a")
    output2 = open("memory_max/flip_vertical.txt", "a")
    output1.write(response.headers["memory_spike"] + " ")
    output1.close()
    output2.write(response.headers["memory_peak"] + " ")
    output2.close()


def test_patch_rotate_c_ok(json_edit_image, memory_header):
    url = address + "rotate-clockwise"
    req_json = json_edit_image
    req_headers = memory_header

    req = Request('PATCH', url, json=req_json, headers=req_headers)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    assert response.status_code == 200

    output1 = open("memory_delta/rotate_clockwise.txt", "a")
    output2 = open("memory_max/rotate_clockwise.txt", "a")
    output1.write(response.headers["memory_spike"] + " ")
    output1.close()
    output2.write(response.headers["memory_peak"] + " ")
    output2.close()


def test_patch_rotate_cc_ok(json_edit_image, memory_header):
    url = address + "rotate-cclockwise"
    req_json = json_edit_image
    req_headers = memory_header

    req = Request('PATCH', url, json=req_json, headers=req_headers)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    assert response.status_code == 200

    output1 = open("memory_delta/rotate_cclockwise.txt", "a")
    output2 = open("memory_max/rotate_cclockwise.txt", "a")
    output1.write(response.headers["memory_spike"] + " ")
    output1.close()
    output2.write(response.headers["memory_peak"] + " ")
    output2.close()


def test_patch_rotate_180_ok(json_edit_image, memory_header):
    url = address + "rotate-180"
    req_json = json_edit_image
    req_headers = memory_header

    req = Request('PATCH', url, json=req_json, headers=req_headers)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    assert response.status_code == 200

    output1 = open("memory_delta/rotate_180.txt", "a")
    output2 = open("memory_max/rotate_180.txt", "a")
    output1.write(response.headers["memory_spike"] + " ")
    output1.close()
    output2.write(response.headers["memory_peak"] + " ")
    output2.close()

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


# flip image
def test_patch_flip_horizontal_empty_json():
    url = address + "flip-horizontal"
    req_json = json.loads('{}')

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_patch_flip_vertical_empty_json():
    url = address + "flip-vertical"
    req_json = json.loads('{}')

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_patch_flip_horziontal_no_image(json_edit_image):
    url = address + "flip-horizontal"
    req_json = json.loads('{}')
    req_json["images_paths"] = ["3.jpeg"]

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["invalid_images"][0] == "3.jpeg"


def test_patch_flip_vertical_no_image(json_edit_image):
    url = address + "flip-vertical"
    req_json = json.loads('{}')
    req_json["images_paths"] = ["3.jpeg"]

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["invalid_images"][0] == "3.jpeg"


@pytest.mark.performance
def test_patch_flip_horziontal_ok(json_edit_image):
    url = address + "flip-horizontal"
    req_json = json_edit_image

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_images"][0] == LOCAL_IMAGES_PATH + "1.jpeg"
    assert json_reponse["valid_images"][1] == LOCAL_IMAGES_PATH + "2.jpeg"

    output = open("performance/flip_horziontal.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()


@pytest.mark.performance
def test_patch_flip_vertical_ok(json_edit_image):
    url = address + "flip-vertical"
    req_json = json_edit_image

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_images"][0] == LOCAL_IMAGES_PATH + "1.jpeg"
    assert json_reponse["valid_images"][1] == LOCAL_IMAGES_PATH + "2.jpeg"

    output = open("performance/flip_vertical.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()


# rotate image
def test_patch_rotate_c_empty_json():
    url = address + "rotate-clockwise"
    req_json = json.loads('{}')

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_patch_rotate_cc_empty_json():
    url = address + "rotate-cclockwise"
    req_json = json.loads('{}')

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_patch_rotate_180_empty_json():
    url = address + "rotate-180"
    req_json = json.loads('{}')

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_patch_rotate_c_no_image(json_edit_image):
    url = address + "rotate-clockwise"
    req_json = json.loads('{}')
    req_json["images_paths"] = ["3.jpeg"]

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["invalid_images"][0] == "3.jpeg"


def test_patch_rotate_cc_no_image(json_edit_image):
    url = address + "rotate-cclockwise"
    req_json = json.loads('{}')
    req_json["images_paths"] = ["3.jpeg"]

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["invalid_images"][0] == "3.jpeg"


def test_patch_rotate_180_no_image(json_edit_image):
    url = address + "rotate-180"
    req_json = json.loads('{}')
    req_json["images_paths"] = ["3.jpeg"]

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["invalid_images"][0] == "3.jpeg"


@pytest.mark.performance
def test_patch_rotate_c_ok(json_edit_image):
    url = address + "rotate-clockwise"
    req_json = json_edit_image

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_images"][0] == LOCAL_IMAGES_PATH + "1.jpeg"
    assert json_reponse["valid_images"][1] == LOCAL_IMAGES_PATH + "2.jpeg"

    output = open("performance/rotate_clockwise.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()


@pytest.mark.performance
def test_patch_rotate_cc_ok(json_edit_image):
    url = address + "rotate-cclockwise"
    req_json = json_edit_image

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_images"][0] == LOCAL_IMAGES_PATH + "1.jpeg"
    assert json_reponse["valid_images"][1] == LOCAL_IMAGES_PATH + "2.jpeg"

    output = open("performance/rotate_cclockwise.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()


@pytest.mark.performance
def test_patch_rotate_180_ok(json_edit_image):
    url = address + "rotate-180"
    req_json = json_edit_image

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_images"][0] == LOCAL_IMAGES_PATH + "1.jpeg"
    assert json_reponse["valid_images"][1] == LOCAL_IMAGES_PATH + "2.jpeg"

    output = open("performance/rotate_180.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()

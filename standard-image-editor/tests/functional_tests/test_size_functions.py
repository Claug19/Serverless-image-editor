import json
import pytest
import sys
from requests import Request, Session

session = Session()
address = "http://127.0.0.1:8004/"

# path building variables
RESOURCES_PATH = "../../resources/"
IMAGES_PATH = "images/"
OUTPUT_PATH = "output/"

# local paths
LOCAL_IMAGES_PATH = RESOURCES_PATH + IMAGES_PATH
LOCAL_OUTPUT_PATH = RESOURCES_PATH + OUTPUT_PATH


@pytest.fixture()
def json_size_image() -> json:
    data = json.loads('{}')
    data["image_path"] = "1.jpeg"
    data["new_height"] = 400
    data["new_width"] = 200
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


# resize image
def test_patch_resize_empty_json():
    url = address + "resize-image"
    req_json = json.loads('{}')

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: image_path"


def test_patch_resize_empty_height(json_size_image):
    url = address + "resize-image"
    req_json = json_size_image;
    del req_json["new_height"]

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: new_height"


def test_patch_resize_empty_width(json_size_image):
    url = address + "resize-image"
    req_json = json_size_image;
    del req_json["new_width"]

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: new_width"


def test_patch_resize_wrong_height_and_width_type(json_size_image):
    url = address + "resize-image"
    req_json = json_size_image;
    req_json["new_height"] = "wrong_value"
    req_json["new_width"] = "wrong_value"

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Invalid new_width or new_height! Skipping entry.."


def test_patch_resize_wrong_image_path(json_size_image):
    url = address + "resize-image"
    req_json = json_size_image;
    req_json["image_path"] = "3.jpeg"

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Image could not be processed!"
    assert json_reponse["invalid_image"] == "3.jpeg"


@pytest.mark.performance
def test_patch_resize_image_ok(json_size_image):
    url = address + "resize-image"
    req_json = json_size_image

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "Image processed successfully!"
    assert json_reponse["resized_image"] == LOCAL_OUTPUT_PATH + "1_resized.jpeg"

    output = open("performance/resize_image.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()

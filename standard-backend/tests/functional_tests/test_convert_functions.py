import json
import pytest
import sys
from requests import Request, Session

session = Session()
address = "http://127.0.0.1:8001/"

# path building variables
RESOURCES_PATH = "../../resources/"
IMAGES_PATH = "images/"
OUTPUT_PATH = "output/"

# local paths
LOCAL_IMAGES_PATH = RESOURCES_PATH + IMAGES_PATH
LOCAL_OUTPUT_PATH = RESOURCES_PATH + OUTPUT_PATH


@pytest.fixture()
def json_convert_image() -> json:
    data = json.loads('{}')
    data["images_paths"] = ["1.jpeg", "2.jpeg"]
    data["format"] = ".png"
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


# convert image
def test_patch_convert_type_empty_json():
    url = address + "convert-type"
    req_json = json.loads('{}')

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_patch_convert_type_no_format(json_convert_image):
    url = address + "convert-type"
    req_json = json_convert_image;
    del req_json["format"]

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: format"


def test_patch_convert_type_wrong_format(json_convert_image):
    url = address + "convert-type"
    req_json = json_convert_image;
    req_json["format"] = "wrong_format"

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: invalid parameter: format"
    assert json_reponse["details"] == req_json["format"] + " is not a supported image extension"


def test_patch_convert_type_missing_image(json_convert_image):
    url = address + "convert-type"
    req_json = json_convert_image
    req_json["images_paths"].append("3.jpeg")

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["valid_converted_images"][0] == LOCAL_OUTPUT_PATH + "1.png"
    assert json_reponse["valid_converted_images"][1] == LOCAL_OUTPUT_PATH + "2.png"
    assert json_reponse["invalid_images"][0] == "3.jpeg"


@pytest.mark.performance
def test_patch_convert_type_ok(json_convert_image):
    url = address + "convert-type"
    req_json = json_convert_image

    req = Request('PATCH', url, json=req_json)
    prepared_request = req.prepare()
    print_PATCH(prepared_request)

    response = session.send(prepared_request)
    print_PATCH_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_converted_images"][0] == LOCAL_OUTPUT_PATH + "1.png"
    assert json_reponse["valid_converted_images"][1] == LOCAL_OUTPUT_PATH + "2.png"

    output = open("performance/convert_type.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()

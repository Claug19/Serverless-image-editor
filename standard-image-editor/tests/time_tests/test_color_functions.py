import json
import pytest
import sys
from requests import Request, Session

session = Session()
address = "http://127.0.0.1:8000/"

# path building variables
RESOURCES_PATH = "../../resources/"
IMAGES_PATH = "images/"
OUTPUT_PATH = "output/"

# local paths
LOCAL_IMAGES_PATH = RESOURCES_PATH + IMAGES_PATH
LOCAL_OUTPUT_PATH = RESOURCES_PATH + OUTPUT_PATH


@pytest.fixture()
def json_color_codes() -> json:
    data = json.loads('{}')
    data["images_paths"] = ["1.jpeg", "2.jpeg"]
    data["occurrence_threshold"] = 1000
    return data


@pytest.fixture()
def json_rgb() -> json:
    data = json.loads('{}')
    data["images_paths"] = ["1.jpeg", "2.jpeg"]
    data["greyscale_flag"] = False
    return data


def print_POST(req):
    print('\n{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------REQ-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body
    ))


def print_POST_resp(resp):
    print('\n{}\n{}\n{}'.format(
        '-----------RESP-----------',
        resp.status_code,
        resp.content
    ))


def test_post_create_color_codes_text_ok(json_color_codes):
    url = address + "color-codes-text"
    req_json = json_color_codes

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    assert response.status_code == 200

    output = open("performance/color_codes_text.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()


def test_post_create_color_codes_chart_ok(json_color_codes):
    url = address + "color-codes-chart"
    req_json = json_color_codes

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    assert response.status_code == 200

    output = open("performance/color_codes_chart.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()


def test_post_create_rgb_channels_ok(json_rgb):
    url = address + "rgb-channels"
    req_json = json_rgb

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    assert response.status_code == 200

    output = open("performance/rgb_channels.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()


def test_post_create_rgb_histogram_ok(json_rgb):
    url = address + "rgb-histogram"
    req_json = json_rgb

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    assert response.status_code == 200

    output = open("performance/rgb_histogram.txt", "a")
    output.write(response.headers["total_time"] + " ")
    output.close()

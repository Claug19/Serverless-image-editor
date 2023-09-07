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


# color text
def test_post_create_color_codes_text_empty_json():
    url = address + "color-codes-text"
    req_json = json.loads('{}')

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_post_create_color_codes_text_missing_image(json_color_codes):
    url = address + "color-codes-text"
    req_json = json_color_codes
    req_json["images_paths"].append("3.jpeg")

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["valid_text_files"][0] == LOCAL_OUTPUT_PATH + "1_colorcodes.txt"
    assert json_reponse["valid_text_files"][1] == LOCAL_OUTPUT_PATH + "2_colorcodes.txt"
    assert json_reponse["invalid_paths"][0] == "3.jpeg"


def test_post_create_color_codes_text_no_treshold_ok(json_color_codes):
    url = address + "color-codes-text"
    req_json = json_color_codes
    del req_json["occurrence_threshold"]

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_text_files"][0] == LOCAL_OUTPUT_PATH + "1_colorcodes.txt"
    assert json_reponse["valid_text_files"][1] == LOCAL_OUTPUT_PATH + "2_colorcodes.txt"


def test_post_create_color_codes_text_ok(json_color_codes):
    url = address + "color-codes-text"
    req_json = json_color_codes

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_text_files"][0] == LOCAL_OUTPUT_PATH + "1_colorcodes.txt"
    assert json_reponse["valid_text_files"][1] == LOCAL_OUTPUT_PATH + "2_colorcodes.txt"


# color chart
def test_post_create_color_codes_chart_empty_json():
    url = address + "color-codes-chart"
    req_json = json.loads('{}')

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_post_create_color_codes_chart_missing_image(json_color_codes):
    url = address + "color-codes-chart"
    req_json = json_color_codes
    req_json["images_paths"].append("3.jpeg")

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["valid_outputs"][0] == LOCAL_OUTPUT_PATH + "1_colorchart.png"
    assert json_reponse["valid_outputs"][1] == LOCAL_OUTPUT_PATH + "2_colorchart.png"
    assert json_reponse["invalid_paths"][0] == "3.jpeg"


def test_post_create_color_codes_chart_no_treshold_ok(json_color_codes):
    url = address + "color-codes-chart"
    req_json = json_color_codes
    del req_json["occurrence_threshold"]

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_outputs"][0] == LOCAL_OUTPUT_PATH + "1_colorchart.png"
    assert json_reponse["valid_outputs"][1] == LOCAL_OUTPUT_PATH + "2_colorchart.png"


def test_post_create_color_codes_chart_ok(json_color_codes):
    url = address + "color-codes-chart"
    req_json = json_color_codes

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_outputs"][0] == LOCAL_OUTPUT_PATH + "1_colorchart.png"
    assert json_reponse["valid_outputs"][1] == LOCAL_OUTPUT_PATH + "2_colorchart.png"


# rgb channels
def test_post_create_rgb_channels_text_empty_json():
    url = address + "rgb-channels"
    req_json = json.loads('{}')

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_post_create_rgb_channels_missing_image(json_rgb):
    url = address + "rgb-channels"
    req_json = json_rgb
    req_json["images_paths"].append("3.jpeg")

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["valid_channels"][0] == LOCAL_OUTPUT_PATH + "1_Rchannel.jpeg"
    assert json_reponse["valid_channels"][1] == LOCAL_OUTPUT_PATH + "1_Gchannel.jpeg"
    assert json_reponse["valid_channels"][2] == LOCAL_OUTPUT_PATH + "1_Bchannel.jpeg"
    assert json_reponse["valid_channels"][3] == LOCAL_OUTPUT_PATH + "2_Rchannel.jpeg"
    assert json_reponse["valid_channels"][4] == LOCAL_OUTPUT_PATH + "2_Gchannel.jpeg"
    assert json_reponse["valid_channels"][5] == LOCAL_OUTPUT_PATH + "2_Bchannel.jpeg"
    assert json_reponse["invalid_paths"][0] == "3.jpeg"


def test_post_create_rgb_channels_grayscale_flag(json_rgb):
    url = address + "rgb-channels"
    req_json = json_rgb
    req_json["greyscale_flag"] = True

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_channels"][0] == LOCAL_OUTPUT_PATH + "1_Rchannel.jpeg"
    assert json_reponse["valid_channels"][1] == LOCAL_OUTPUT_PATH + "1_Gchannel.jpeg"
    assert json_reponse["valid_channels"][2] == LOCAL_OUTPUT_PATH + "1_Bchannel.jpeg"
    assert json_reponse["valid_channels"][3] == LOCAL_OUTPUT_PATH + "2_Rchannel.jpeg"
    assert json_reponse["valid_channels"][4] == LOCAL_OUTPUT_PATH + "2_Gchannel.jpeg"
    assert json_reponse["valid_channels"][5] == LOCAL_OUTPUT_PATH + "2_Bchannel.jpeg"


def test_post_create_rgb_channels_ok(json_rgb):
    url = address + "rgb-channels"
    req_json = json_rgb

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_channels"][0] == LOCAL_OUTPUT_PATH + "1_Rchannel.jpeg"
    assert json_reponse["valid_channels"][1] == LOCAL_OUTPUT_PATH + "1_Gchannel.jpeg"
    assert json_reponse["valid_channels"][2] == LOCAL_OUTPUT_PATH + "1_Bchannel.jpeg"
    assert json_reponse["valid_channels"][3] == LOCAL_OUTPUT_PATH + "2_Rchannel.jpeg"
    assert json_reponse["valid_channels"][4] == LOCAL_OUTPUT_PATH + "2_Gchannel.jpeg"
    assert json_reponse["valid_channels"][5] == LOCAL_OUTPUT_PATH + "2_Bchannel.jpeg"


# rgb histogram
def test_post_create_rgb_histogram_empty_json():
    url = address + "rgb-histogram"
    req_json = json.loads('{}')

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Bad Request: missing mandatory parameter: images_paths"


def test_post_create_rgb_histogram_missing_image(json_rgb):
    url = address + "rgb-histogram"
    req_json = json_rgb
    req_json["images_paths"].append("3.jpeg")

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 400
    assert json_reponse["error"] == "Some images could not be processed!"
    assert json_reponse["valid_histograms"][0] == LOCAL_OUTPUT_PATH + "1_Rplot.png"
    assert json_reponse["valid_histograms"][1] == LOCAL_OUTPUT_PATH + "1_Gplot.png"
    assert json_reponse["valid_histograms"][2] == LOCAL_OUTPUT_PATH + "1_Bplot.png"
    assert json_reponse["valid_histograms"][3] == LOCAL_OUTPUT_PATH + "1_RGBplot.png"
    assert json_reponse["valid_histograms"][4] == LOCAL_OUTPUT_PATH + "2_Rplot.png"
    assert json_reponse["valid_histograms"][5] == LOCAL_OUTPUT_PATH + "2_Gplot.png"
    assert json_reponse["valid_histograms"][6] == LOCAL_OUTPUT_PATH + "2_Bplot.png"
    assert json_reponse["valid_histograms"][7] == LOCAL_OUTPUT_PATH + "2_RGBplot.png"
    assert json_reponse["invalid_paths"][0] == "3.jpeg"


def test_post_create_rgb_histogram_ok(json_rgb):
    url = address + "rgb-histogram"
    req_json = json_rgb

    req = Request('POST', url, json=req_json)
    prepared_request = req.prepare()
    print_POST(prepared_request)

    response = session.send(prepared_request)
    print_POST_resp(response)

    json_reponse = json.loads(response.content)
    assert response.status_code == 200
    assert json_reponse["message"] == "All images processed successfully!"
    assert json_reponse["valid_histograms"][0] == LOCAL_OUTPUT_PATH + "1_Rplot.png"
    assert json_reponse["valid_histograms"][1] == LOCAL_OUTPUT_PATH + "1_Gplot.png"
    assert json_reponse["valid_histograms"][2] == LOCAL_OUTPUT_PATH + "1_Bplot.png"
    assert json_reponse["valid_histograms"][3] == LOCAL_OUTPUT_PATH + "1_RGBplot.png"
    assert json_reponse["valid_histograms"][4] == LOCAL_OUTPUT_PATH + "2_Rplot.png"
    assert json_reponse["valid_histograms"][5] == LOCAL_OUTPUT_PATH + "2_Gplot.png"
    assert json_reponse["valid_histograms"][6] == LOCAL_OUTPUT_PATH + "2_Bplot.png"
    assert json_reponse["valid_histograms"][7] == LOCAL_OUTPUT_PATH + "2_RGBplot.png"

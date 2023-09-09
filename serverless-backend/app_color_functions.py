# packages
import time
import tracemalloc
from flask import Flask, request, g
from flask_lambda import FlaskLambda

# local
import common_functions as common
import file_manager as fm
import handler_color_codes
import handler_rgb_channels
import handler_rgb_histograms


common.log("Lambda FLASK: color")
app = FlaskLambda(__name__)


@app.before_request
def setup_procedure():
    common.log("setup " + request.method + " " +request.path)
    # memory
    if request.headers.get("Memory-Test") == "True":
        tracemalloc.start()
    # time
    g.start_time = time.perf_counter()


@app.after_request
def teardown_procedure(response):
    common.log("teardown " + request.method + " " +request.path)
    # time
    total_time = time.perf_counter() - g.start_time
    time_in_ms = int(total_time * 1000)
    common.log('Request took {} seconds (milliseconds: {}) {} {}'
               .format(total_time, time_in_ms, request.method, request.path))
    response.headers['total_time'] = total_time
    # memory
    if request.headers.get("Memory-Test") == "True":
        memory_current, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        response.headers['memory_spike'] = memory_peak - memory_current
        response.headers['memory_peak'] = memory_peak
    return response


# routes
@app.route('/color-codes-text', methods=['POST'])
def post_create_color_codes_text() -> tuple:
    common.log(post_create_color_codes_text.__name__)
    mandatory_parameters = ["images_paths"]
    optional_parameters = {"occurrence_threshold": 500}

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    for optional_parameter in list(optional_parameters.keys()):
        if optional_parameter in request.json:
            optional_parameters[optional_parameter] = request.json[optional_parameter]

    return handler_color_codes.handle_post_color_codes_text(images_paths, optional_parameters)


@app.route('/color-codes-chart', methods=['POST'])
def post_create_color_codes_chart() -> tuple:
    common.log(post_create_color_codes_chart.__name__)
    mandatory_parameters = ["images_paths"]
    optional_parameters = {"occurrence_threshold": 500}

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    for optional_parameter in list(optional_parameters.keys()):
        if optional_parameter in request.json:
            optional_parameters[optional_parameter] = request.json[optional_parameter]

    return handler_color_codes.handle_post_color_codes_chart(images_paths, optional_parameters)


@app.route('/rgb-channels', methods=['POST'])
def post_create_rgb_channels() -> tuple:
    common.log(post_create_rgb_channels.__name__)
    mandatory_parameters = ["images_paths"]
    optional_parameters = {"greyscale_flag": False}

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    for optional_parameter in list(optional_parameters.keys()):
        if optional_parameter in request.json:
            optional_parameters[optional_parameter] = request.json[optional_parameter]

    return handler_rgb_channels.handle_post_rgb_channels(images_paths, optional_parameters)


@app.route('/rgb-histogram', methods=['POST'])
def post_create_rgb_histograms() -> tuple:
    common.log(post_create_rgb_histograms.__name__)
    mandatory_parameters = ["images_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    return handler_rgb_histograms.handle_post_rgb_histograms(images_paths)

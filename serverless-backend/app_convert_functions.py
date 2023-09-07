# packages
import os
import time
import tracemalloc
from flask import Flask, request, g
from flask_lambda import FlaskLambda
from flask_swagger_ui import get_swaggerui_blueprint

# local
import common_functions as common
import file_manager as fm
import handler_convert_images


common.log("Lambda FLASK: convert")
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
    common.log("setup " + request.method + " " +request.path)
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


# app_convert_functions swagger
SWAGGER_URL = '/swagger-convert'
API_URL = '/static/swagger_convert.json'

SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "app_convert_functions"})

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


# routes
@app.route('/convert-type', methods=['PATCH'])
def patch_convert_type() -> tuple:
    common.log(patch_convert_type.__name__)
    mandatory_parameters = ["images_paths", "format"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]
    new_format = request.json["format"]

    if not common.validate_image_format(new_format):
        parameter = "format"
        details = new_format + " is not a supported image extension"
        return common.respond_bad_request_invalid(parameter, details)

    return handler_convert_images.handle_patch_convert_image(images_paths, new_format)

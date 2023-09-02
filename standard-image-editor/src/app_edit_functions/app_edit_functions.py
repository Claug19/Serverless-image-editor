# packages
import sys
import time
import tracemalloc
from flask import Flask, request, g
from flask_lambda import FlaskLambda
from flask_swagger_ui import get_swaggerui_blueprint

sys.path.append('../..')

# local
from src.common import common_functions as common, file_manager as fm
from handlers import (
    handler_flip_images,
    handler_rotate_images
)

# app_edit_functions flask
if fm.get_configuration() == "LOCAL":
    common.log("Local FLASK")
    app = Flask(__name__)
else:
    common.log("Lambda FLASK")
    app = FlaskLambda(__name__)


@app.before_request
def setup_procedure():
    # memory
    if request.headers.get("Memory-Test") == "True":
        tracemalloc.start()
    # time
    g.start_time = time.perf_counter()


@app.after_request
def teardown_procedure(response):
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


# app_edit_functions swagger
SWAGGER_URL = '/swagger-edit'
API_URL = '/static/swagger_edit.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "app_edit_functions"})

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


# get profiling decorator
conditional_profiling = common.get_conditional_profiling()


# routes
@app.route('/flip-horizontal', methods=['PATCH'])
@conditional_profiling
def patch_flip_horizontal() -> tuple:
    common.log(patch_flip_horizontal.__name__)
    mandatory_parameters = ["images_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    return handler_flip_images.handle_patch_flip_image(images_paths, True)


@app.route('/flip-vertical', methods=['PATCH'])
@conditional_profiling
def patch_flip_vertical() -> tuple:
    common.log(patch_flip_vertical.__name__)
    mandatory_parameters = ["images_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    return handler_flip_images.handle_patch_flip_image(images_paths, False)


@app.route('/rotate-clockwise', methods=['PATCH'])
@conditional_profiling
def patch_rotate_clockwise() -> tuple:
    common.log(patch_rotate_clockwise.__name__)
    mandatory_parameters = ["images_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    return handler_rotate_images.handle_patch_rotate_image(images_paths, "clockwise")


@app.route('/rotate-cclockwise', methods=['PATCH'])
@conditional_profiling
def patch_rotate_counter_clockwise() -> tuple:
    common.log(patch_rotate_counter_clockwise.__name__)
    mandatory_parameters = ["images_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    return handler_rotate_images.handle_patch_rotate_image(images_paths, "cclockwise")


@app.route('/rotate-180', methods=['PATCH'])
@conditional_profiling
def patch_rotate_180() -> tuple:
    common.log(patch_rotate_180.__name__)
    mandatory_parameters = ["images_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    images_paths = request.json["images_paths"]

    return handler_rotate_images.handle_patch_rotate_image(images_paths, "180")


if __name__ == '__main__':
    common.check_bucket()
    app.run(host="0.0.0.0", debug=True, port=8002)

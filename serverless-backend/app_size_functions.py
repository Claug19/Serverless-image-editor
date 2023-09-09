# packages
import time
import tracemalloc
from flask import Flask, request, g
from flask_lambda import FlaskLambda

# local
import common_functions as common
import file_manager as fm
import handler_resize_image


common.log("Lambda FLASK: size")
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
@app.route('/resize-image', methods=['PATCH'])
def patch_resize_image() -> tuple:
    common.log(patch_resize_image.__name__)
    mandatory_parameters = ["image_path", "new_height", "new_width"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    image_paths = request.json["image_path"]
    new_height = request.json["new_height"]
    new_width = request.json["new_width"]

    return handler_resize_image.handle_patch_resize_image(image_paths, new_height, new_width)

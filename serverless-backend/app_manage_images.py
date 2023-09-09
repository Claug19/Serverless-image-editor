# packages
import base64
import time
import tracemalloc
from flask import Flask, request, g
from flask_lambda import FlaskLambda

# local
import common_functions as common
import file_manager as fm
import handler_manage_images


common.log("Lambda FLASK: manage")
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


@app.route('/add-image', methods=['POST'])
def post_add_image() -> tuple:
    common.log(post_add_image.__name__)

    mandatory_parameters = ["name", "content"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request.json:
            return common.respond_bad_request_missing(mandatory_parameter)

    file_name = request.json["name"]
    file_content = base64.b64decode(request.json["content"])

    if file_name == '':
        common.log('Error: No selected file')
        return common.respond_bad_request_missing('filename')

    if file_content == '':
        common.log('Error: Empty file')
        return common.respond_bad_request_missing('file content')

    extension = file_name.split('.')[1]

    if not common.validate_image_format("." + extension):
        parameter = "format"
        details = extension + " is not a supported image extension"
        return common.respond_bad_request_invalid(parameter, details)

    # save  to s3
    return handler_manage_images.handle_add_image(file_name, file_content, extension)

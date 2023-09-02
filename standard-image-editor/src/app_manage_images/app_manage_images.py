import json
from flask import Flask, request
from flask_lambda import FlaskLambda

from src.common import common_functions as common, file_manager as fm
from handlers import handler_manage_images

if fm.get_configuration() == "LOCAL":
    print(" Local conf: FLASK")
    app = Flask(__name__)
else:
    print(fm.get_configuration(), "FlaskLambda")
    app = FlaskLambda(__name__)


@app.route('/env-setup', methods=['POST'])
def post_environment_setup() -> tuple:
    common.log(post_environment_setup.__name__)
    mandatory_parameters = ["environment"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request:
            return common.respond_bad_request_missing(mandatory_parameter)

    environment = request["environment"]

    return ()


@app.route('/post-images', methods=['POST'])
def post_images(request: str) -> tuple:
    req = json.loads(request)
    common.log(post_images.__name__)

    return handler_manage_images.add_images(req)


@app.route('/get-images', methods=['GET'])
def get_images(request: json) -> tuple:
    common.log(get_images.__name__)
    mandatory_parameters = ["image_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request:
            return common.respond_bad_request_missing(mandatory_parameter)

    image_paths = request["image_paths"]

    return ()


@app.route('/get-all-images', methods=['GET'])
def get_all_images() -> tuple:
    common.log(get_all_images.__name__)

    return ()


@app.route('/delete-images', methods=['DELETE'])
def delete_images(request: json) -> tuple:
    common.log(delete_images.__name__)
    mandatory_parameters = ["image_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request:
            return common.respond_bad_request_missing(mandatory_parameter)

    image_paths = request["image_paths"]

    return ()


@app.route('/delete-all-images', methods=['DELETE'])
def delete_all_images() -> tuple:
    common.log(delete_all_images.__name__)

    return ()


@app.route('/get-outputs', methods=['GET'])
def get_outputs(request: json) -> tuple:
    common.log(get_outputs.__name__)
    mandatory_parameters = ["output_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request:
            return common.respond_bad_request_missing(mandatory_parameter)

    output_paths = request["output_paths"]

    return ()


@app.route('/get-all-outputs', methods=['GET'])
def get_all_outputs() -> tuple:
    common.log(get_all_outputs.__name__)

    return ()


if __name__ == '__main__':
    common.check_bucket()
    app.run(host="0.0.0.0", debug=True, port=8003)

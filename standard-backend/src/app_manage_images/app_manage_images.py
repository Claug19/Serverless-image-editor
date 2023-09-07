# packages
import sys
from flask import Flask, request
from flask_lambda import FlaskLambda

sys.path.append('../..')

# local
from src.common import common_functions as common, file_manager as fm
from handlers import handler_manage_images

if fm.get_configuration() == "LOCAL":
    print(" Local conf: FLASK")
    app = Flask(__name__)
else:
    print(fm.get_configuration(), "FlaskLambda")
    app = FlaskLambda(__name__)



@app.route('/post-image', methods=['POST'])
def post_image() -> tuple:
    common.log(post_image.__name__)
     if 'file' not in request.files:
            error = 'No file part'
            common.log(error)
            return common.respond_bad_request_missing('file')
        file = request.files['file']
        
        if file.filename == '':
            common.log('No selected file')
            return common.respond_bad_request_missing('filename')

    # save  to s3
    return handler_manage_images.add_images(req)


@app.route('/get-image', methods=['GET'])
def get_image() -> tuple:
    common.log(get_image.__name__)
    return ()


@app.route('/delete-image', methods=['DELETE'])
def delete_image() -> tuple:
    common.log(delete_image.__name__)
    return ()


@app.route('/get-outputs', methods=['GET'])
def get_outputs() -> tuple:
    common.log(get_outputs.__name__)
    mandatory_parameters = ["output_paths"]

    for mandatory_parameter in mandatory_parameters:
        if mandatory_parameter not in request:
            return common.respond_bad_request_missing(mandatory_parameter)

    output_paths = request["output_paths"]

    return ()

if __name__ == '__main__':
    common.check_bucket()
    app.run(host="0.0.0.0", debug=True, port=8003)

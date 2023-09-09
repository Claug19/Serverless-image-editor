# packages
import io
import json
from PIL import Image

# local
import common_functions as common
import file_manager as fm


def handle_add_image(file_name: str, file_content: str, extension: str) -> tuple:
    common.log("Uploading image:" + file_name)

    output_path = fm.convert_image_path_to_env(file_name)

    file_buffer = io.BytesIO(file_content)

    image = Image.open(file_buffer)

    try:
        fm.write_image_to_s3(image, output_path, extension)
        data = {"message": "Image uploaded successfully!"}
        return json.dumps(data), 200, {'Content-Type': 'application/json'}
    except:
        data = {"error": "Image could not be uploaded!"}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}

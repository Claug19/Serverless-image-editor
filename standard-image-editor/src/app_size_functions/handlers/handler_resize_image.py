# packages
import json
import sys
from PIL import Image

sys.path.append('../..')

# local
from src.common import common_functions as common, file_manager as fm


def handle_patch_resize_image(image_path: str, new_height: int, new_width: int) -> tuple:
    if not isinstance(image_path, str):
        error = "Invalid file name! Skipping entry.."
        common.log(error)
        data = {"error": error}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}

    if not isinstance(new_height, int) or \
            not isinstance(new_width, int):
        error = "Invalid new_width or new_height! Skipping entry.."
        common.log(error)
        data = {"error": error}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}

    if resize_image(image_path, new_height, new_width):
        data = {"message": "Image processed successfully!",
                "resized_image": get_resized_image(image_path)}
        return json.dumps(data), 200, {'Content-Type': 'application/json'}
    else:
        data = {"error": "Image could not be processed!",
                "invalid_image": image_path}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}


def resize_image(image_path: str, new_height: int, new_width: int) -> bool:
    if not common.check_image_existence(image_path):
        return False
    common.log("Processing image:" + fm.convert_full_image_path_to_env(image_path))

    # input/output variables
    image_path_no_ext = image_path.split('.')[0]
    extension = image_path.split('.')[1]
    output_path = fm.convert_output_path_to_env(image_path_no_ext + "_resized." + extension)
    image_path = fm.convert_image_path_to_env(image_path)

    # input
    input_image = None
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        input_image = Image.open(image_path)

    if fm.get_configuration() == "AWS":
        input_image = fm.read_image_from_s3(image_path)

    # process
    resized_image = input_image.resize((new_width, new_height))

    # output
    if fm.get_configuration() == "LOCAL":
        resized_image.save(output_path)

    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        fm.write_image_to_s3(resized_image, output_path, extension)

    return True


def get_resized_image(image_path: str) -> str:
    image_path_no_ext = image_path.split('.')[0]
    extension = image_path.split('.')[1]
    return fm.get_env_full_output_path() + image_path_no_ext + "_resized." + extension

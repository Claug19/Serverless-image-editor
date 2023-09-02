# packages
import json
from PIL import Image

# local
import common_functions as common
import file_manager as fm


def handle_patch_convert_image(images_paths: list, new_format: str) -> tuple:
    valid_output = []
    invalid_output = []
    processed_all_entries = True

    for image_path in images_paths:
        if not isinstance(image_path, str):
            common.log("Invalid file name! Skipping entry..")
            invalid_output.append(image_path)
            processed_all_entries = False
            continue
        if convert_image(image_path, new_format):
            valid_output.append(get_valid_converted_image(image_path, new_format))
        else:
            invalid_output.append(image_path)
            processed_all_entries = False

    if processed_all_entries:
        data = {"message": "All images processed successfully!",
                "valid_converted_images": valid_output}
        return json.dumps(data), 200, {'Content-Type': 'application/json'}
    else:
        data = {"error": "Some images could not be processed!",
                "valid_converted_images": valid_output,
                "invalid_images": invalid_output}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}


def convert_image(image_path: str, new_format: str) -> bool:
    if not common.check_image_existence(image_path):
        return False
    common.log("Processing image:" + fm.convert_full_image_path_to_env(image_path))

    # input/output variables
    image_path_no_ext = image_path.split('.')[0]
    output_path = fm.convert_output_path_to_env(image_path_no_ext + new_format)
    image_path = fm.convert_image_path_to_env(image_path)

    # input
    input_image = None
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        input_image = Image.open(image_path)

    if fm.get_configuration() == "AWS":
        input_image = fm.read_image_from_s3(image_path)

    # process
    image = input_image.convert('RGB')

    # output
    if fm.get_configuration() == "LOCAL":
        image.save(output_path)

    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        fm.write_image_to_s3(image, output_path, new_format[1:])
    return True


def get_valid_converted_image(image_path: str, new_format: str) -> str:
    image_path_no_ext = image_path.split('.')[0]
    output_path = image_path_no_ext + new_format
    return fm.get_env_full_output_path() + output_path

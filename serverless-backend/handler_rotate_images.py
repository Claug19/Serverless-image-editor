# packages
import cv2
import json
import numpy as np
from io import BytesIO

# local
import common_functions as common
import file_manager as fm


def handle_patch_rotate_image(images_paths: list, amount: str) -> tuple:
    valid_output = []
    invalid_output = []
    processed_all_entries = True

    for image_path in images_paths:
        if not isinstance(image_path, str):
            common.log("Invalid file name! Skipping entry..")
            invalid_output.append(image_path)
            processed_all_entries = False
            continue
        if rotate_image(image_path, amount):
            valid_output.append(fm.convert_full_image_path_to_env(image_path))
        else:
            invalid_output.append(image_path)
            processed_all_entries = False

    if processed_all_entries:
        data = {"message": "All images processed successfully!",
                "valid_images": valid_output}
        return json.dumps(data), 200, {'Content-Type': 'application/json'}
    else:
        data = {"error": "Some images could not be processed!",
                "valid_images": valid_output,
                "invalid_images": invalid_output}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}


def rotate_image(image_path: str, amount: str) -> bool:
    if not common.check_image_existence(image_path):
        return False
    common.log("Processing image: " + fm.convert_full_image_path_to_env(image_path))

    # input/output variables
    image_format = "." + image_path.split('.')[1]
    image_path = fm.convert_image_path_to_env(image_path)
    output_path = image_path

    # input
    input_image = None
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        input_image = cv2.imread(image_path)

    if fm.get_configuration() == "AWS":
        image = fm.read_image_from_s3(image_path)
        input_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # process
    rotated_image = None
    if amount == "clockwise" or not amount:
        rotated_image = cv2.rotate(input_image, cv2.ROTATE_90_CLOCKWISE)
    if amount == "cclockwise":
        rotated_image = cv2.rotate(input_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if amount == "180":
        rotated_image = cv2.rotate(input_image, cv2.ROTATE_180)

    # output
    if fm.get_configuration() == "LOCAL":
        cv2.imwrite(output_path, rotated_image)

    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        is_success, image_buffer = cv2.imencode(image_format, rotated_image)
        io_image_buffer = BytesIO(image_buffer)
        fm.write_image_buffer_to_s3(io_image_buffer, output_path, image_format[1:])

    cv2.imwrite(output_path, rotated_image)

    return True

# packages
import cv2
import json
import numpy as np
from io import BytesIO

# local
import common_functions as common
import file_manager as fm


def handle_post_rgb_channels(images_paths: list, optional_parameters: dict) -> tuple:
    valid_output = []
    invalid_output = []
    processed_all_entries = True

    greyscale_flag = optional_parameters["greyscale_flag"]

    for image_path in images_paths:
        if not isinstance(image_path, str):
            common.log("Invalid file name! Skipping entry..")
            invalid_output.append(image_path)
            processed_all_entries = False
            continue
        if generate_rgb_channels(image_path, greyscale_flag):
            valid_output.extend(get_valid_channels(image_path))
        else:
            invalid_output.append(image_path)
            processed_all_entries = False

    if processed_all_entries:
        data = {"message": "All images processed successfully!",
                "valid_channels": valid_output}
        return json.dumps(data), 200, {'Content-Type': 'application/json'}
    else:
        data = {"error": "Some images could not be processed!",
                "valid_channels": valid_output,
                "invalid_paths": invalid_output}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}


def generate_rgb_channels(image_path: str, greyscale_flag: bool) -> bool:
    if not common.check_image_existence(image_path):
        return False
    common.log("Processing image:" + fm.convert_full_image_path_to_env(image_path))

    # input/output variables
    image_format = "." + image_path.split('.')[1]
    output_r_channel = fm.convert_output_path_to_env(image_path.replace('.', '_Rchannel.'))
    output_g_channel = fm.convert_output_path_to_env(image_path.replace('.', '_Gchannel.'))
    output_b_channel = fm.convert_output_path_to_env(image_path.replace('.', '_Bchannel.'))
    image_path = fm.convert_image_path_to_env(image_path)

    # input
    input_image = None
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        input_image = cv2.imread(image_path)

    if fm.get_configuration() == "AWS":
        image = fm.read_image_from_s3(image_path)
        input_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # process
    # configuration variables after reading image
    red_channel_image = np.zeros(input_image.shape, np.uint8)
    green_channel_image = np.zeros(input_image.shape, np.uint8)
    blue_channel_image = np.zeros(input_image.shape, np.uint8)

    blue_mask, green_mask, red_mask = cv2.split(input_image)

    red_channel_image[:, :, 2] = red_mask
    green_channel_image[:, :, 1] = green_mask
    blue_channel_image[:, :, 0] = blue_mask

    # output
    if fm.get_configuration() == "LOCAL":
        if greyscale_flag is True:
            cv2.imwrite(output_r_channel, red_mask)
            cv2.imwrite(output_g_channel, green_mask)
            cv2.imwrite(output_b_channel, blue_mask)
        else:
            cv2.imwrite(output_r_channel, red_channel_image)
            cv2.imwrite(output_g_channel, green_channel_image)
            cv2.imwrite(output_b_channel, blue_channel_image)

    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        if greyscale_flag is True:
            is_success, red_buffer = cv2.imencode(image_format, red_mask)
            is_success, green_buffer = cv2.imencode(image_format, green_mask)
            is_success, blue_buffer = cv2.imencode(image_format, blue_mask)
        else:
            is_success, red_buffer = cv2.imencode(image_format, red_channel_image)
            is_success, green_buffer = cv2.imencode(image_format, green_channel_image)
            is_success, blue_buffer = cv2.imencode(image_format, blue_channel_image)
        io_red_buffer = BytesIO(red_buffer)
        io_green_buffer = BytesIO(green_buffer)
        io_blue_buffer = BytesIO(blue_buffer)
        fm.write_image_buffer_to_s3(io_red_buffer, output_r_channel, image_format[1:])
        fm.write_image_buffer_to_s3(io_green_buffer, output_g_channel, image_format[1:])
        fm.write_image_buffer_to_s3(io_blue_buffer, output_b_channel, image_format[1:])

    return True


def get_valid_channels(image_path: str) -> list:
    output_r_channel = image_path.replace('.', '_Rchannel.')
    output_g_channel = image_path.replace('.', '_Gchannel.')
    output_b_channel = image_path.replace('.', '_Bchannel.')
    return [fm.get_env_full_output_path() + output_r_channel,
            fm.get_env_full_output_path() + output_g_channel,
            fm.get_env_full_output_path() + output_b_channel]

# packages
import cv2
import json
import numpy as np
import sys
from io import BytesIO
from matplotlib import pyplot as plt

sys.path.append('../..')

# local
from src.common import common_functions as common, file_manager as fm


def handle_post_rgb_histograms(images_paths: list) -> tuple:
    valid_output = []
    invalid_output = []
    processed_all_entries = True

    for image_path in images_paths:
        if not isinstance(image_path, str):
            common.log("Invalid file name! Skipping entry..")
            invalid_output.append(image_path)
            processed_all_entries = False
            continue
        if generate_rgb_histograms(image_path):
            valid_output.extend(get_valid_histograms(image_path))
        else:
            invalid_output.append(image_path)
            processed_all_entries = False

    if processed_all_entries:
        data = {"message": "All images processed successfully!",
                "valid_histograms": valid_output}
        return json.dumps(data), 200, {'Content-Type': 'application/json'}
    else:
        data = {"error": "Some images could not be processed!",
                "valid_histograms": valid_output,
                "invalid_paths": invalid_output}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}


def generate_rgb_histograms(image_path: str) -> bool:
    if not common.check_image_existence(image_path):
        return False
    common.log("Processing image: " + fm.convert_full_image_path_to_env(image_path))

    # configuration variables
    default_dpi = 1000
    default_rgb_bins = range(0, 256, 1)
    default_rgb_xtics = range(0, 256, 15)
    default_rgb_range = [0, 256]
    default_figszie = (7, 7)

    # input/output variables
    image_path_no_ext = image_path.split('.')[0]
    output_r_plot = fm.convert_output_path_to_env(image_path_no_ext + '_Rplot.png')
    output_g_plot = fm.convert_output_path_to_env(image_path_no_ext + '_Gplot.png')
    output_b_plot = fm.convert_output_path_to_env(image_path_no_ext + '_Bplot.png')
    output_rgb_plot = fm.convert_output_path_to_env(image_path_no_ext + '_RGBplot.png')
    image_path = fm.convert_image_path_to_env(image_path)

    # input
    input_image = None
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        input_image = cv2.imread(image_path)

    if fm.get_configuration() == "AWS":
        image = fm.read_image_from_s3(image_path)
        input_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # process
    blue_mask, green_mask, red_mask = cv2.split(input_image)

    # generate red mask histogram figure
    red_plot = plt.figure(figsize=default_figszie)
    plt.xticks(default_rgb_xtics)
    plt.hist(red_mask.ravel(), default_rgb_bins, default_rgb_range, color='red')

    # generate green mask histogram figure
    green_plot = plt.figure(figsize=default_figszie)
    plt.xticks(default_rgb_xtics)
    plt.hist(green_mask.ravel(), default_rgb_bins, default_rgb_range, color='green')

    # generate blue mask histogram figure
    blue_plot = plt.figure(figsize=default_figszie)
    plt.xticks(default_rgb_xtics)
    plt.hist(blue_mask.ravel(), default_rgb_bins, default_rgb_range, color='blue')

    # generate RGB mask histogram
    rgb_plot = plt.figure(figsize=default_figszie)
    plt.xticks(default_rgb_xtics)
    plt.hist(red_mask.ravel(), default_rgb_bins, default_rgb_range, histtype="step", color='red')
    plt.hist(green_mask.ravel(), default_rgb_bins, default_rgb_range, histtype="step", color='green')
    plt.hist(blue_mask.ravel(), default_rgb_bins, default_rgb_range, histtype="step", color='blue')

    # output
    if fm.get_configuration() == "LOCAL":
        red_plot.savefig(output_r_plot, dpi=default_dpi)
        green_plot.savefig(output_g_plot, dpi=default_dpi)
        blue_plot.savefig(output_b_plot, dpi=default_dpi)
        rgb_plot.savefig(output_rgb_plot, dpi=default_dpi)

    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        red_buffer = BytesIO()
        green_buffer = BytesIO()
        blue_buffer = BytesIO()
        rgb_buffer = BytesIO()
        red_plot.savefig(red_buffer, dpi=default_dpi, format='png')
        green_plot.savefig(green_buffer, dpi=default_dpi, format='png')
        blue_plot.savefig(blue_buffer, dpi=default_dpi, format='png')
        rgb_plot.savefig(rgb_buffer, dpi=default_dpi, format='png')
        fm.write_image_buffer_to_s3(red_buffer, output_r_plot, 'png')
        fm.write_image_buffer_to_s3(green_buffer, output_g_plot, 'png')
        fm.write_image_buffer_to_s3(blue_buffer, output_b_plot, 'png')
        fm.write_image_buffer_to_s3(rgb_buffer, output_rgb_plot, 'png')

    plt.close('all')
    return True


def get_valid_histograms(image_path: str) -> list:
    image_path_no_ext = image_path.split('.')[0]
    output_r_plot = image_path_no_ext + '_Rplot.png'
    output_g_plot = image_path_no_ext + '_Gplot.png'
    output_b_plot = image_path_no_ext + '_Bplot.png'
    output_rgb_plot = image_path_no_ext + '_RGBplot.png'
    return [fm.get_env_full_output_path() + output_r_plot,
            fm.get_env_full_output_path() + output_g_plot,
            fm.get_env_full_output_path() + output_b_plot,
            fm.get_env_full_output_path() + output_rgb_plot]

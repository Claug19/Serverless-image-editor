# packages
import cv2
import json
import numpy as np
import matplotlib
from io import BytesIO, StringIO 

# local
import common_functions as common
import file_manager as fm

matplotlib.use('agg')


def handle_post_color_codes_text(images_paths: list, optional_parameters: dict) -> tuple:
    valid_output = []
    invalid_output = []
    processed_all_entries = True

    occurrence_threshold = optional_parameters["occurrence_threshold"]

    for image_path in images_paths:
        if not isinstance(image_path, str):
            common.log("Invalid file name! Skipping entry..")
            invalid_output.append(image_path)
            processed_all_entries = False
            continue
        if generate_color_codes_text(image_path, occurrence_threshold):
            valid_output.extend(get_valid_outputs_text(image_path))
        else:
            invalid_output.append(image_path)
            processed_all_entries = False

    if processed_all_entries:
        data = {"message": "All images processed successfully!",
                "valid_text_files": valid_output}
        return json.dumps(data), 200, {'Content-Type': 'application/json'}
    else:
        data = {"error": "Some images could not be processed!",
                "valid_text_files": valid_output,
                "invalid_paths": invalid_output}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}


def handle_post_color_codes_chart(images_paths: list, optional_parameters: dict) -> tuple:
    valid_output = []
    invalid_output = []
    processed_all_entries = True

    occurrence_threshold = optional_parameters["occurrence_threshold"]

    for image_path in images_paths:
        if not isinstance(image_path, str):
            common.log("Invalid file name! Skipping entry..")
            invalid_output.append(image_path)
            processed_all_entries = False
            continue
        if generate_color_codes_chart(image_path, occurrence_threshold):
            valid_output.extend(get_valid_outputs_chart(image_path))
        else:
            invalid_output.append(image_path)
            processed_all_entries = False

    if processed_all_entries:
        data = {"message": "All images processed successfully!",
                "valid_outputs": valid_output}
        return json.dumps(data), 200, {'Content-Type': 'application/json'}
    else:
        data = {"error": "Some images could not be processed!",
                "valid_outputs": valid_output,
                "invalid_paths": invalid_output}
        return json.dumps(data), 400, {'Content-Type': 'application/json'}


def generate_color_codes_text(image_path: str, occurrence_threshold: int) -> bool:
    if not common.check_image_existence(image_path):
        return False
    common.log("Processing image:" + fm.convert_full_image_path_to_env(image_path))

    # input/output variables
    image_path_no_ext = image_path.split('.')[0]
    output_color_occurrences_txt = fm.convert_output_path_to_env(image_path_no_ext + '_colorcodes.txt')
    image_path = fm.convert_image_path_to_env(image_path)

    # input
    input_image = None
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        input_image = cv2.imread(image_path)

    if fm.get_configuration() == "AWS":
        image = fm.read_image_from_s3(image_path)
        input_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # process
    occurrences_dict = {}
    for pixelGroup in input_image:
        for pixel in pixelGroup:
            hex_color = '#%02x%02x%02x' % (pixel[2], pixel[1], pixel[0])
            occurrences_dict[hex_color] = occurrences_dict.get(hex_color, 0) + 1

    color_occurrence_file = None
    if fm.get_configuration() == "LOCAL":
        color_occurrence_file = open(output_color_occurrences_txt, "w")

    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        color_occurrence_file = StringIO()

    for occurrenceEntry in list(occurrences_dict.keys()):
        if occurrences_dict.get(occurrenceEntry) <= occurrence_threshold:
            del occurrences_dict[occurrenceEntry]

    occurrences_dict = dict(sorted(occurrences_dict.items(), key=lambda item: item[1]))

    line_counter = 0
    for dictEntry in list(occurrences_dict.keys()):
        color_occurrence_file.write(str(dictEntry) + ": " + str(occurrences_dict.get(dictEntry)) + ", ")
        if line_counter == 9:
            line_counter = 0
            color_occurrence_file.write("\n")
        else:
            line_counter += 1

    # output
    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        # save color codes
        fm.write_text_to_s3(color_occurrence_file.getvalue(), output_color_occurrences_txt)

    color_occurrence_file.close()
    return True


def generate_color_codes_chart(image_path: str, occurrence_threshold: int) -> bool:
    if not common.check_image_existence(image_path):
        return False
    common.log("Processing image:" + fm.convert_full_image_path_to_env(image_path))

    # configuration_variables
    default_dpi = 1000
    default_figszie = (7, 7)

    # input/output variables
    image_path_no_ext = image_path.split('.')[0]
    output_color_occurrences_txt = fm.convert_output_path_to_env(image_path_no_ext + '_colorcodes.txt')
    output_color_codes_chart = fm.convert_output_path_to_env(image_path_no_ext + '_colorchart.png')
    image_path = fm.convert_image_path_to_env(image_path)

    # input
    input_image = None
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        input_image = cv2.imread(image_path)

    if fm.get_configuration() == "AWS":
        image = fm.read_image_from_s3(image_path)
        input_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # process
    occurrences_dict = {}
    for pixelGroup in input_image:
        for pixel in pixelGroup:
            hex_color = '#%02x%02x%02x' % (pixel[2], pixel[1], pixel[0])
            occurrences_dict[hex_color] = occurrences_dict.get(hex_color, 0) + 1

    color_occurrence_file = None
    if fm.get_configuration() == "LOCAL":
        color_occurrence_file = open(output_color_occurrences_txt, "w")

    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        color_occurrence_file = StringIO()

    for occurrenceEntry in list(occurrences_dict.keys()):
        if occurrences_dict.get(occurrenceEntry) <= occurrence_threshold:
            del occurrences_dict[occurrenceEntry]

    occurrences_dict = dict(sorted(occurrences_dict.items()))

    line_counter = 0
    for dictEntry in list(occurrences_dict.keys()):
        color_occurrence_file.write(str(dictEntry) + ": " + str(occurrences_dict.get(dictEntry)) + ", ")
        if line_counter == 9:
            line_counter = 0
            color_occurrence_file.write("\n")
        else:
            line_counter += 1

    color_chart = matplotlib.pyplot.figure(figsize=default_figszie)
    matplotlib.pyplot.pie(occurrences_dict.values(), colors=list(occurrences_dict.keys()))

    # output
    if fm.get_configuration() == "LOCAL":
        color_chart.savefig(output_color_codes_chart, dpi=default_dpi)

    if fm.get_configuration() == "AWS" or fm.get_configuration() == "LOCAL-AWS":
        # save color codes
        fm.write_text_to_s3(color_occurrence_file.getvalue(), output_color_occurrences_txt)

        # save chart
        chart_buffer = BytesIO()
        color_chart.savefig(chart_buffer, dpi=default_dpi, format='png')
        fm.write_image_buffer_to_s3(chart_buffer, output_color_codes_chart, 'png')

    color_occurrence_file.close()
    matplotlib.pyplot.close('all')
    return True


def get_valid_outputs_text(image_path: str) -> list:
    image_path_no_ext = image_path.split('.')[0]
    output_colors_txt = image_path_no_ext + '_colorcodes.txt'
    return [fm.get_env_full_output_path() + output_colors_txt]


def get_valid_outputs_chart(image_path: str) -> list:
    image_path_no_ext = image_path.split('.')[0]
    output_colors_image = image_path_no_ext + '_colorchart.png'
    return [fm.get_env_full_output_path() + output_colors_image]

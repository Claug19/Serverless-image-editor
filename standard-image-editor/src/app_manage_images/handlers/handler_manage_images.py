import json
import sys

sys.path.append('../..')

from src.common import file_manager as fm


def add_images(req: json) -> tuple:
    valid_output = []
    invalid_output = []

    creation_response = fm.create_images(req["files"])

    for image_entry in creation_response:
        if creation_response[image_entry] == "failed":
            invalid_output.append(image_entry)
        if creation_response[image_entry] == "ok":
            valid_output.append(image_entry)

    if len(invalid_output):
        data = {}

    print(created_images)
    return ();


def remove_images(image_paths: list) -> tuple:
    valid_output = []
    invalid_output = []
    processed_all_entries = True
    
    for image_path in images_paths:
        if not isinstance(image_path, str):
            print("Invalid file name! Skipping entry..")
            invalid_output.append(image_path)
            processed_all_entries = False
            continue
        if generate_rgb_histograms(image_path):
            valid_output.extend(get_valid_histograms(image_path))
        else:
            invalid_output.append(image_path)
            processed_all_entries = False
    
    if processed_all_entries:
        data = {"message" : "All images processed successfully!",
                "valid_histograms" : valid_output}
        return (json.dumps(data), 200, {'Content-Type': 'application/json'})
    else:
        data = {"error" : "Some images could not be processed!",
                "valid_histograms" : valid_output,
                "invalid_paths": invalid_output}
        return (json.dumps(data), 400, {'Content-Type': 'application/json'})


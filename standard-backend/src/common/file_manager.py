import base64
import boto3
import json
import os
import sys
from io import BytesIO

import botocore
from PIL import Image

sys.path.append('..')

# local
from src.common import configuration, common_functions as common

# ===========================
#       paths variables
# ===========================

# path building variables
RESOURCES_PATH = "../../resources/"
IMAGES_PATH = "images/"
OUTPUT_PATH = "output/"

# local paths
LOCAL_IMAGES_PATH = RESOURCES_PATH + IMAGES_PATH
LOCAL_OUTPUT_PATH = RESOURCES_PATH + OUTPUT_PATH

# aws paths
AWS_BUCKET_PATH = "https://" + configuration.AWS_S3_BUCKET_NAME + ".s3." + configuration.AWS_REGION + ".amazonaws.com/"
AWS_BUCKET_IMAGES_PATH = AWS_BUCKET_PATH + IMAGES_PATH
AWS_BUCKET_OUTPUT_PATH = AWS_BUCKET_PATH + OUTPUT_PATH

# microsoft paths
MICROSOFT_CONTAINER_PATH = ".."
MICROSOFT_CONTAINER_IMAGES_PATH = MICROSOFT_CONTAINER_PATH + IMAGES_PATH
MICROSOFT_CONTAINER_OUTPUT_PATH = MICROSOFT_CONTAINER_PATH + OUTPUT_PATH


# =======================================
#       get configuration variables
# =======================================
def get_configuration() -> str:
    return configuration.CURRENT_ENV


def get_bucket_name() -> str:
    return configuration.AWS_S3_BUCKET_NAME


def get_aws_region() -> str:
    return configuration.AWS_REGION


def get_profile_flag() -> bool:
    return configuration.PROFILING_FLAG


# ==========================
#       paths managing
# ==========================

# without url
def get_env_images_path() -> str:
    if get_configuration() == "AWS":
        return IMAGES_PATH
    if get_configuration() == "LOCAL" or get_configuration() == "LOCAL-AWS":
        return LOCAL_IMAGES_PATH
    if get_configuration() == "MS":
        return IMAGES_PATH
    return ""


# with entire url
def get_env_full_images_path() -> str:
    if get_configuration() == "AWS":
        return AWS_BUCKET_IMAGES_PATH
    if get_configuration() == "LOCAL" or get_configuration() == "LOCAL-AWS":
        return LOCAL_IMAGES_PATH
    if get_configuration() == "MS":
        return MICROSOFT_CONTAINER_IMAGES_PATH
    return ""


# without url
def get_env_output_path() -> str:
    if get_configuration() == "AWS" or get_configuration() == "LOCAL-AWS":
        return OUTPUT_PATH
    if get_configuration() == "LOCAL":
        return LOCAL_OUTPUT_PATH
    if get_configuration() == "MS":
        return OUTPUT_PATH
    return ""


# with entire url
def get_env_full_output_path() -> str:
    if get_configuration() == "AWS" or get_configuration() == "LOCAL-AWS":
        return AWS_BUCKET_OUTPUT_PATH
    if get_configuration() == "LOCAL":
        return LOCAL_OUTPUT_PATH
    if get_configuration() == "MS":
        return MICROSOFT_CONTAINER_OUTPUT_PATH
    return ""


def convert_image_path_to_env(received_path: str) -> str:
    return get_env_images_path() + received_path


def convert_full_image_path_to_env(received_path: str) -> str:
    return get_env_full_images_path() + received_path


def convert_output_path_to_env(received_path: str) -> str:
    return get_env_output_path() + received_path


def convert_full_output_path_to_env(received_path: str) -> str:
    return get_env_full_output_path() + received_path


# ===========================
#       bucket managing
# ===========================
def read_image_from_s3(key: str):
    s3 = boto3.resource('s3', region_name=get_aws_region())
    bucket = s3.Bucket(get_bucket_name())
    bucket_object = bucket.Object(key)
    response = bucket_object.get()
    file_stream = response['Body']
    return Image.open(file_stream)


def write_image_to_s3(image, key: str, new_format: str):
    s3_client = boto3.client('s3')
    file_stream = BytesIO()
    image.save(file_stream, format=new_format)
    try:
        s3_client.put_object(Body=file_stream.getvalue(), Bucket=get_bucket_name(), Key=key,
                             ContentType='image/' + new_format)
    except botocore.exceptions.ClientError as error:
        # Put your error handling logic here
        common.log(error)
        raise error


def write_image_buffer_to_s3(image_buffer, key: str, new_format: str):
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=image_buffer.getvalue(), Bucket=get_bucket_name(), Key=key,
                         ContentType='image/' + new_format)


def write_text_to_s3(text, key: str):
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=text, Bucket=get_bucket_name(), Key=key,
                         ContentType='text/plain')


# ==========================
#       image managing
# ==========================
def check_or_create_mandatory_directories() -> bool:
    os.makedirs(os.path.dirname(get_env_images_path()), exist_ok=True)
    os.makedirs(os.path.dirname(get_env_output_path()), exist_ok=True)
    images_check_path = os.path.isdir(get_env_images_path())
    output_check_path = os.path.isdir(get_env_output_path())
    return images_check_path and output_check_path


def create_images(images_json: json) -> json:
    response_dict = json.loads('{}')

    if not check_or_create_mandatory_directories():
        response_dict["error"] = "mandatory directories not present"
        return response_dict

    for image_entry in images_json:
        image_path = convert_image_path_to_env(image_entry)
        output_image = open(image_path, 'wb')

        # decode image from base64
        decoded_image = base64.b64decode(images_json[image_entry].split(",")[1])
        output_image.write(decoded_image)
        output_image.close()
        created_image = os.path.exists(image_path)
        if created_image:
            response_dict[image_path] = "ok"
        else:
            response_dict[image_path] = "failed"

    return response_dict


def get_images(image_paths: list) -> json:
    response_dict = json.loads('{}')

    if not check_or_create_mandatory_directories():
        response_dict["error"] = "mandatory directories not present"
        return response_dict

    for image_path in image_paths:
        complete_image_path = convert_image_path_to_env(image_path)
        if os.path.exists(complete_image_path):
            response_dict[image_path] = open(complete_image_path, "rb").read()
        else:
            response_dict[image_path] = "not found"
    return response_dict


def delete_images(image_paths: list) -> json:
    response_dict = json.loads('{}')

    if not check_or_create_mandatory_directories():
        response_dict["error"] = "mandatory directories not present"
        return response_dict

    for image_path in image_paths:
        complete_image_path = convert_image_path_to_env(image_path)
        if os.path.exists(complete_image_path):
            os.remove(complete_image_path)
            response_dict[image_path] = "removed"
        else:
            response_dict[image_path] = "not found"
    return response_dict


def get_outputs(file_paths: list) -> json:
    response_dict = json.loads('{}')

    if not check_or_create_mandatory_directories():
        response_dict["error"] = "mandatory directories not present"
        return response_dict

    for file_path in file_paths:
        complete_file_path = convert_output_path_to_env(file_path)
        if os.path.exists(complete_file_path):
            response_dict[file_path] = open(complete_file_path, "rb").read()
        else:
            response_dict[file_path] = "not found"
    return response_dict

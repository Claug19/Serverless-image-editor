# packages
import boto3
import botocore
import logging
import json
import sys
from botocore.exceptions import ClientError
from datetime import datetime
from memory_profiler import profile
from os.path import exists

sys.path.append('..')

# local
import src.common.file_manager as fm


s3_client = boto3.client('s3')

# bucket functions
def check_bucket() -> bool:
    bucket_name_str = fm.get_bucket_name()

    foundBucket = False

    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        if bucket["Name"] == bucket_name_str:
             foundBucket = True

    if foundBucket == True:
        log("Found images-editor bucket")
        s3_client.put_object(Bucket=bucket_name_str, Key=('images/'))
        s3_client.put_object(Bucket=bucket_name_str, Key=('output/'))
        return True
    result = create_bucket(bucket_name=bucket_name_str)
    if result == False:
        return False
    s3_client.put_object(Bucket=bucket_name_str, Key=('images/'))
    s3_client.put_object(Bucket=bucket_name_str, Key=('output/'))
    return True

def create_bucket(bucket_name):
    region = fm.get_aws_region()
    location = {'LocationConstraint': region}
    try:
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        log("Creating_bucket:", bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# logger function
def log(string_to_log: str):
    if fm.get_configuration() == "AWS":
        print("", datetime.now(), string_to_log, flush=True)
    if fm.get_configuration() == "MS":
        print("", datetime.now(), string_to_log, flush=True)
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        print("", datetime.now(), string_to_log, flush=True)


# utility functions
def validate_image_format(format: str) -> bool:
    valid_formats = [".jpeg", ".png", ".ppm", ".gif", ".tiff", ".bmp"]
    if format not in valid_formats:
        return False
    return True


def empty_decorator(func):
    # empty decorator used for profiling flag disabled
    return func


def get_conditional_profiling():
    return profile if fm.get_profile_flag() else empty_decorator


# generic rest responses
def respond_bad_request_missing(parameter: str) -> tuple:
    data = {"error" : "Bad Request: missing mandatory parameter: " + parameter}
    return (json.dumps(data), 400, {'Content-Type': 'application/json'})


def respond_bad_request_invalid(parameter: str, details: str) -> tuple:
    data = {"error" : "Bad Request: invalid parameter: " + parameter,
            "details" : details}
    return (json.dumps(data), 400, {'Content-Type': 'application/json'})


# handler functions
# utility functions
def check_image_existence(image_path: str) -> bool:
    log(check_image_existence.__name__ + ": " + fm.convert_image_path_to_env(image_path))
    if fm.get_configuration() == "LOCAL" or fm.get_configuration() == "LOCAL-AWS":
        if not exists(fm.convert_image_path_to_env(image_path)):
            log("check_image_existence: Image " + image_path + " not found, skipping path..")
            return False
        return True

    if fm.get_configuration() == "AWS":
        s3 = boto3.resource('s3')
        try:
            s3.Object(fm.get_bucket_name(), fm.convert_image_path_to_env(image_path)).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                log("check_image_existence: " + image_path + " : error 404 NOT FOUND")
                return False
            else:
                log("check_image_existence: exception")
                raise
        else:
            return True

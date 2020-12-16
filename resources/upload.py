import boto3
import uuid
import os

from flask import request, render_template, make_response
from flask_restful import Resource
from werkzeug.utils import secure_filename

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

# Establish s3 client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  )


class Upload(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template("file-upload.html"))

    @classmethod
    def post(cls):
        img = request.files["file"]
        if img:
            unique = str(uuid.uuid4())
            split_name = img.filename.split(".")
            name = split_name[0]
            file_ext = split_name[1]

            unique_name = secure_filename(unique + "-" + name)  # Generates unique name.
            unique_filename = unique_name + "." + file_ext  # Generates video filename.
            m3u8_filename = unique_name + ".m3u8"  # Generates HLS filename.

            img.save(unique_filename)

            key = "assets01/" + unique_filename  # Uploads into specific folder to trigger the AWS Lambda function.
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=unique_filename,
                Key=key
            )
            # Remove the file from the local file system after uploading to s3.
            os.remove(unique_filename)
            # Generates the link to the cdn which the frontend can uses to pull the on demand video.
            cdn_link = "https://d11rse4z1ry9t6.cloudfront.net/" + unique_name + "/AppleHLS1/" + m3u8_filename
            print(cdn_link)
            return make_response(render_template("upload-success.html", response="successful"))
        return make_response(render_template("upload-success.html", response="unsuccessful"))

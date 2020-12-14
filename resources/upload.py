import os, boto3

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
            filename = secure_filename(img.filename)
            img.save(filename)
            key = "assets01/" + filename # Will upload into specific folder.
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=key
            )
            # Remove the file from the local file system after uploading to s3.
            os.remove(filename)
            return make_response(render_template("upload-success.html", response="successful"))
        return make_response(render_template("upload-success.html", response="unsuccessful"))

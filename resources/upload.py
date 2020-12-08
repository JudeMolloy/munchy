import os, boto3

from flask import request, render_template, make_response
from flask_restful import Resource
from werkzeug.utils import secure_filename

# Establish s3 client
s3 = boto3.client('s3',
                  aws_access_key_id='access key here',
                  aws_secret_access_key='secret key here',
                  aws_session_token='secret token here'
                  )

BUCKET_NAME = os.environ.get("BUCKET_NAME")


class Upload(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template("file-upload.html"))

    @classmethod
    def post(cls):
        # aws code not finished yet!!!
        img = request.files["file"]
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )
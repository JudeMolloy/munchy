import boto3
import uuid
import os

from werkzeug.utils import secure_filename

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
VOD_SOURCE_BUCKET_NAME = os.environ.get("VOD_SOURCE_BUCKET_NAME")

# Establish s3 client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  )


def upload_to_vod_bucket(video):
    unique = str(uuid.uuid4())
    split_name = video.filename.split(".")
    name = split_name[0]
    file_ext = split_name[1]

    # COULD ADD A FILE TYPE CHECK HERE. MIGHT LEAVE THIS FOR SIMPLICITY JUST NOW.

    unique_name = secure_filename(unique + "-" + name)  # Generates unique name.
    unique_filename = unique_name + "." + file_ext  # Generates video filename.
    m3u8_filename = unique_name + ".m3u8"  # Generates HLS filename.

    video.save(unique_filename)

    key = "assets01/" + unique_filename  # Uploads into specific folder to trigger the AWS Lambda function.
    s3.upload_file(
        Bucket=str(VOD_SOURCE_BUCKET_NAME),
        Filename=unique_filename,
        Key=key
    )

    # Remove the file from the local file system after uploading to s3.
    os.remove(unique_filename)
    # Generates the link to the cdn which the frontend can uses to pull the on demand video.
    cdn_link = "https://d11rse4z1ry9t6.cloudfront.net/" + unique_name + "/AppleHLS1/" + m3u8_filename

    return cdn_link
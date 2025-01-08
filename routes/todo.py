import os
from fastapi import  UploadFile, File, HTTPException,APIRouter
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
from helper.helper_funtions import extract_note_identifier

# Load environment variables from .env file
load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

router = APIRouter()

# Initialize the S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


@router.post("/upload-to-s3")
async def upload_to_s3(file: UploadFile = File(...)):
    """
    Uploads a file to the specified S3 bucket and returns its public URL.
    """
    # print(file)
    try:
        '''# Define the S3 object key (file path in the bucket)
        object_name = file.filename

        # Upload the file to S3
        s3_client.upload_fileobj(
            file.file,  # File object from UploadFile
            AWS_BUCKET_NAME,  # Target bucket name
            object_name,  # S3 object name (key) # Set the file to be publicly readable
        )
        file_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": AWS_BUCKET_NAME, "Key": object_name},
            ExpiresIn=3600  # 1 hour validity
        )'''
        print(type(file.file))
        note_number=await extract_note_identifier(file.file)
        return {"message": "File uploaded successfully", "note_number": note_number}

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

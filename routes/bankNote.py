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

UPLOAD_FOLDER = "uploaded_files"

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)





@router.post("/exract_number")
async def exract_number(file: UploadFile = File(...)):
    
    try:
       
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        # file.save("uploaded_files/img.jpg")
        note_number=await extract_note_identifier(file_path)
        return {"message": "File uploaded successfully", "note_number": note_number}

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        # Delete the saved file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

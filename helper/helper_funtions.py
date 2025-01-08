from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException,status,Header,Depends,UploadFile, File
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta, timezone
import cv2
import pytesseract
from typing import Optional
import os
import numpy as np
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# import pytesseract
from PIL import Image, ExifTags
from re import match
import easyocr


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"





def convert_objectid(doc):
    if doc:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)







def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=float(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,os.getenv("SECRET_KEY") , algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


# Define HTTPBearer for JWT Token
security = HTTPBearer()

# Dependency to extract and verify the token
def get_token_headers(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Extract the token
    return verify_jwt_token(token)
    
def verify_jwt_token(jwt_token):
    try:
        if not jwt_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="jwt_token header missing")
        # if not jwt_token.startswith("Bearer "):
        #     print(jwt_token)
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid jwt_token header format",token=jwt_token)
        # token=jwt_token.split(" ")[1]  # Extract the token after "Bearer "
        payload = jwt.decode(jwt_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail= f"Invalid token {e}") from e
    



# Configure Tesseract path if needed (Windows users)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_orientation(image):
    # Open the image
    image = Image.open(image)
    
    # Handle EXIF orientation if it exists
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        
        exif = image._getexif()
        if exif is not None and orientation in exif:
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"EXIF metadata processing error: {e}")
    
    # Get dimensions
    width, height = image.size
    
    # Determine orientation
    if width > height:
        print("The image is in Landscape orientation.")
        return {'landscape':True,"portrait":False,"width": width,"height": height}
    elif height > width:
        print("The image is in Portrait orientation.")
        return {'landscape':False,"portrait":True,"width": width,"height": height}
    else:
        print("The image is Square.")
        return {'landscape':False,"portrait":False,"width": width,"height": height}

# Replace with your image path


# im_100rs=Image.open("upload/100rs.jpg")
def display(image):
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def greyscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

async def extract_note_identifier(image) -> Optional[str]:
  
    try:
        im_100rs=cv2.imread(image)
        if im_100rs is None:
            print("Error: Image not found or unable to load. Check the file path.")
            exit()






        orientation_obj= get_orientation(image)
        # print (orientation_obj.portrait)
        if orientation_obj["portrait"]:
            # Define the crop region (x, y, width, height)
            x, y, w, h = int(orientation_obj["width"]/2), 0, int(orientation_obj["width"]/2), int(orientation_obj["height"]/2)  # Example coordinates
            cropped_image = im_100rs[y:y+h, x:x+w]
            cropped_image_1=cv2.rotate(cropped_image, cv2.ROTATE_90_CLOCKWISE)
            cropped_image_2=cv2.rotate(cropped_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # display(cropped_image_2)
        elif orientation_obj["landscape"]:
            # Define the crop region (x, y, width, height)
            cropped_image=cv2.rotate(im_100rs, cv2.ROTATE_90_CLOCKWISE)
            x, y, w, h = int(orientation_obj["width"]/2), 0, int(orientation_obj["height"]/2), int(orientation_obj["width"]/2)  # Example coordinates
            cropped_image = cropped_image[y:y+h, x:x+w]
            cropped_image_1=cv2.rotate(cropped_image, cv2.ROTATE_90_CLOCKWISE)
            cropped_image_2=cv2.rotate(cropped_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # display(cropped_image)









        reader = easyocr.Reader([ 'en'],gpu=True)
        grey_img_1 = greyscale(cropped_image_1)
        grey_img_2 = greyscale(cropped_image_2)
        # thresh, im_blackandwhite =cv2.threshold(grey_img, 127, 255, cv2.THRESH_BINARY)
        # memory_img=Image.fromarray(grey_img)

        # text = pytesseract.image_to_string(memory_img,lang="eng")
        text_arr_1  = reader.readtext(grey_img_1,detail = 0)
        text_arr_2  = reader.readtext(grey_img_2,detail = 0)
        # for arr, value,pos in text:
        #     print(f"{value}, {pos}")




        # text_arr= [ *text_arr_1 , *text_arr_2]
        # print(text_arr)





        noteNum_firstpart = list(filter(lambda v: match(r"[0-9]{1}[a-zA-Z]{2}$", v), text_arr_1))
        if noteNum_firstpart:
            noteNum_scoendpart = list(filter(lambda v: match(r"[0-9]{6}$", v), text_arr_1))
        else:
            noteNum_firstpart = list(filter(lambda v: match(r"[0-9]{1}[a-zA-Z]{2}$", v), text_arr_2))
            if noteNum_firstpart:
                noteNum_scoendpart = list(filter(lambda v: match(r"[0-9]{6}$", v), text_arr_2))

        noteNum=noteNum_firstpart[0] + " " + noteNum_scoendpart[0]
        print(noteNum)

    except Exception as e:
        return f"An error occurred: {e}"

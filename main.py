from fastapi import FastAPI, File, UploadFile, Form
import mediapipe as mp
import cv2
from character.detect_shape import face_classifi
from character.skincolor import skin_detect
import os
import numpy as np

app = FastAPI()

@app.get("/")
def read_rood():
    return{"Hello":"World"}

@app.post("/files/")
async def create_file(file: bytes= File(), fileb: UploadFile=File(), token: str=Form()):
    return{
        "file_size":len(file),
        "token":token,
        "fileb_content_type":fileb.content_type
    }

# @app.post("/character")
# def character_fs():
#     image = request.files['file']
#     fshape = face_classifi(image)
#     sColor = skin_detect(image)
    
#     return {"face shape" : fshape,
#             "skin color" : sColor}
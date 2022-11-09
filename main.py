from fastapi import FastAPI, File, Form
import mediapipe as mp
import cv2
from character.detect_shape import face_classifi
from character.skincolor import skin_detect
import io
import numpy as np
from PIL import Image

app = FastAPI()

@app.get("/")
def read_rood():
    return{"Hello":"World"}

@app.post("/files/")
async def create_file(file: bytes= File(...)):
    image = np.array(Image.open(io.BytesIO(file)))
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    fshape = face_classifi(image)
    sColor = skin_detect(image)
    
    return {"face shape" : fshape,
            "skin color" : sColor}
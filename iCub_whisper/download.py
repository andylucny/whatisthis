print('please, wait...')
import requests
import os
from zipfile import ZipFile
from io import BytesIO
import torch
import whisper

def download_espeak():
    if os.path.exists("espeak.exe"):
        return
    print("downloading espeak")
    url = "https://www.agentspace.org/download/espeak.zip"
    response = requests.get(url)
    zip = ZipFile(BytesIO(response.content))
    zip.extractall()
    print("espeak downloaded")

def download_DinoViT_model():
    if os.path.exists("dino_deits8.onnx"):
        return
    print("downloading model")
    url = "https://dl.fbaipublicfiles.com/dino/dino_deitsmall8_pretrain/dino_deits8.onnx"
    response = requests.get(url)
    open("dino_deits8.onnx","wb").write(response.content)
    print("model downloaded")

def download_whisper():    
    whisper.load_model("base.en")

def download_all():
    download_espeak()
    download_DinoViT_model()
    download_whisper()

if __name__ == "__main__":
    download_all()
    print("done")
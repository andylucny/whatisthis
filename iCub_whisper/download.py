print('please, wait...')
import requests
import os
from zipfile import ZipFile
from io import BytesIO
import torch
import whisper

def download_and_save(url,path):
    if os.path.exists(path):
        return
    print("downloading",path)
    response = requests.get(url)
    open(path,"wb").write(response.content)
    print(path,"downloaded")
    
def download_DinoViT_model():
    download_and_save("https://dl.fbaipublicfiles.com/dino/dino_deitsmall8_pretrain/dino_deits8.onnx","dino_deits8.onnx")

def download_LaMini_model():
    if not os.path.exists("LaMini/"):
        os.mkdir("LaMini")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/README.md","LaMini/README.md")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/config.json","LaMini/config.json")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/generation_config.json","LaMini/generation_config.json")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/pytorch_model.bin","LaMini/pytorch_model.bin")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/special_tokens_map.json","LaMini/special_tokens_map.json")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/spiece.model","LaMini/spiece.model")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/tokenizer.json","LaMini/tokenizer.json")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/tokenizer_config.json","LaMini/tokenizer_config.json")
    download_and_save("https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M/resolve/main/training_args.bin","LaMini/training_args.bin")

def download_whisper():    
    whisper.load_model("base.en")
    
def download_all():
    download_DinoViT_model()
    download_LaMini_model()
    download_whisper()

if __name__ == "__main__":
    download_all()
    print("done")
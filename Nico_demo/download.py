print('please, wait...')
import requests
import os
import zipfile
import io

def download_and_save(url,path):
    if os.path.exists(path):
        return
    print("downloading",path)
    response = requests.get(url)
    open(path,"wb").write(response.content)
    print(path,"downloaded")
    
def download_DinoViT_model():
    download_and_save("https://www.agentspace.org/download/dino_deits8-224-final.onnx","dino_deits8.onnx")

def download_robot_config():
    download_and_save("https://www.agentspace.org/download/nico_humanoid_upper_rh7d_ukba.json","nico_humanoid_upper_rh7d_ukba.json")

def download_v4l2(path,url):
    if os.path.exists(path):
        return
    print("downloading",path)
    response = requests.get(url)
    if response.ok:
        file_like_object = io.BytesIO(response.content)
        zipfile_object = zipfile.ZipFile(file_like_object)    
        zipfile_object.extractall(".")

def download_all():
    download_DinoViT_model()
    download_robot_config()
    download_v4l2("v4l2-ctl.exe","https://www.agentspace.org/download/v4l2-ctl.zip")  

if __name__ == "__main__":
    download_all()
    print("done")


from datetime import datetime
import json
import requests
import io
import base64
from PIL import Image
import os
import time
import urllib.request

  

webui_server_url = "http://127.0.0.1:7860"
out_dir_t2i=""
out_dir_i2i=""
stableDiffuionOutPutPath="C:/WorkSpace/SD/stable-diffusion-webui/outputs/"
  

def MakeOutputDir():
    #out_dir = 'api_out'
    global out_dir_t2i
    global out_dir_i2i
    out_dir_t2i = os.path.join(os.path.join(stableDiffuionOutPutPath, 'txt2img-images'),CurrentDate())
    out_dir_i2i = os.path.join(os.path.join(stableDiffuionOutPutPath, 'img2img-images'),CurrentDate())
    os.makedirs(out_dir_t2i, exist_ok=True)
    os.makedirs(out_dir_i2i, exist_ok=True)

def CurrentDate():
    return datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")

  

def timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")


def encode_file_to_base64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def decode_and_save_base64(base64_str, save_path):
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))


def call_api(api_endpoint, **payload):
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        f'{webui_server_url}/{api_endpoint}',
        headers={'Content-Type': 'application/json'},
        data=data,
    )
    response = urllib.request.urlopen(request)
    return json.loads(response.read().decode('utf-8'))


def call_txt2img_api(**payload):
    imagePathList=[]
    response = call_api('sdapi/v1/txt2img', **payload)
    for index, image in enumerate(response.get('images')):
        save_path = os.path.join(out_dir_t2i, f'txt2img-{timestamp()}-{index}.png')
        decode_and_save_base64(image, save_path)
        imagePathList.append(save_path)
    return imagePathList


def call_img2img_api(**payload):
    response = call_api('sdapi/v1/img2img', **payload)
    for index, image in enumerate(response.get('images')):
        save_path = os.path.join(out_dir_i2i, f'img2img-{timestamp()}-{index}.png')
        decode_and_save_base64(image, save_path)



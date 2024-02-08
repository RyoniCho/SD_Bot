import telegramMessage
import sdapi
import sys
import requests

RESPONSE_MAKE_START=1
RESPONSE_EXIT=2
RESPONSE_EXIT_YES=3
RESPONSE_PROMPT=-1
RESPONSE_SHOWSETTINGS=4
RESPONSE_SETSETTINGS=5
RESPONSE_RESET=6
RESPONSE_ADON=7
RESPONSE_ADOFF=8
RESPONSE_HELP=9


helpText ="=======STABLE DIFFUSION BOT========\n"
helpText+="? : 프롬프트 입력시 맨앞에 붙여준다.(wildcard:$value$)\n"
helpText+="생성 : 생성시작시 입력한다.\n"
helpText+="셋팅 : 현재 셋팅을 보여준다.\n"
helpText+="키=값: 셋팅을 바꿀때 사용한다. (ex: width=900)\n"
helpText+="초기화 : 셋팅을 초기화한다..\n"
helpText+="adon : adetailer를 켜준다.\n"
helpText+="adoff : adtailer를 꺼준다.\n"
helpText+="종료 : 봇을 종료한다.\n"


isMaking=False
cachedPayload=dict
defaultPayload = {
        "prompt": "",  
        "negative_prompt": "verybadimagenegative_v1.3",
        "seed": -1,
        "steps": 30,
        "width": 512,
        "height": 768,
        "cfg_scale": 8,
        "sampler_name": "DPM++ 2M Karras",
        "n_iter": 1,
        "batch_size": 1,

        "enable_hr": False,
        "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
        "hr_scale": 2,
        "denoising_strength": 0.4,
        
        # "override_settings": {
        #     'sd_model_checkpoint': "sd_xl_base_1.0",  # this can use to switch sd model
        # },
        "alwayson_scripts": 
        {
            "ADetailer": 
            {
                "args": [
                    {
                        "ad_model": "face_yolov8n.pt"
                    }
                ]
            }
        }
    }

adjson={
            "ADetailer": 
            {
                "args": [
                    {
                        "ad_model": "face_yolov8n.pt"
                    }
                ]
            }
        }

def SetParam(key, value):
    global defaultPayload
    if  key in defaultPayload:
        currentType=type(defaultPayload[key]) 
        if currentType == int:
            defaultPayload[key]=int(value)
        elif currentType == float:
            defaultPayload[key]=float(value)
        elif currentType == bool:
            if value.lower() == "false":
                defaultPayload[key]=False
            elif value.lower()=="true":
                defaultPayload[key]=True
        else:
            defaultPayload[key]=value



def botUpdate(message):
    global defaultPayload
    while True:
        (messageId,txt)=message.CheckMessageInLoop()

        if messageId==RESPONSE_EXIT:
            message.send_message("SD봇을 종료하시겠습니까?(네/아니오)")
        elif messageId==RESPONSE_EXIT_YES:
            message.send_message("SD봇이 종료되었습니다")
            break
        elif messageId == RESPONSE_MAKE_START:
            if isMaking == False:
                Start_Make_SD(message)
            pass
        elif messageId == RESPONSE_PROMPT:
            prompt= txt.replace("?","").replace("$","__")

            defaultPayload["prompt"]=prompt
            message.send_message(f"프롬프트 설정완료: {prompt}")
        elif messageId == RESPONSE_SETSETTINGS:
            splitedText=txt.split("=")
            if splitedText[0] in defaultPayload:
                SetParam(splitedText[0],splitedText[1])
                message.send_message(f"{splitedText[0]}을 {splitedText[1]}로 셋팅하였습니다.\n{defaultPayload}")
            else:
                message.send_message(f"{splitedText[0]} 은 없는 옵션 키값입니다.")

        elif messageId == RESPONSE_SHOWSETTINGS:
            message.send_message(f"현재 셋팅: \n{defaultPayload}")
            pass
        elif messageId == RESPONSE_RESET:
            defaultPayload=cachedPayload.copy()
            message.send_message(f"기본옵션으로 리셋하였습니다\n{defaultPayload}")
            pass
        elif messageId == RESPONSE_ADOFF:
            if "alwayson_scripts" in defaultPayload:
                del defaultPayload["alwayson_scripts"]
                message.send_message(f"adetailer 삭제되었습니다.\n{defaultPayload}")
        elif messageId == RESPONSE_ADON:
            if not "alwayson_scripts" in defaultPayload:
                defaultPayload["alwayson_scripts"]=adjson
                message.send_message(f"adetailer 추가되었습니다.\n{defaultPayload}")
        elif messageId==RESPONSE_HELP:
            message.send_message(helpText)
        



            
    
    sys.exit()

def Start_Make_SD(message):
    sdapi.MakeOutputDir()
    if str(defaultPayload["prompt"]) != "":
        message.send_message("SD Text2Img 생성시작..")
        isMaking=True
        
        imagePathList = sdapi.call_txt2img_api(**defaultPayload)
        if len(imagePathList)>0:
            for image in imagePathList:
                message.send_photo(image)

        message.send_message("SD Text2Img 생성완료")       
        isMaking=False
    else:
        message.send_message("프롬프트가 비어있습니다. 프롬프트를 채워주세요.")
   

if __name__ == '__main__':
    try:
        cachedPayload=defaultPayload.copy()

        # SetParam("enable_hr","true")
        # del defaultPayload["alwayson_scripts"]
        # print(defaultPayload)


        mg = telegramMessage.message()
        mg.send_message(f"SD봇이 시작되었습니다.\n{helpText}")
    

        botUpdate(mg)
    except requests.exceptions.ConnectionError as e:
        print(e)
        if mg is not None:
            mg.send_message("Connection Error발생. 봇이 종료됩니다.")
   
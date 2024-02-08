import requests
import json
import time

class message:
    
    def __init__(self):
        self.token="==Telegram Bot Token=="
        self.my_chat_id="==Telegram Bot ChatID=="
        self.SetInfo()
        self.msgSet=set()
        self.exitPlag=False
        
        self.makeStart=1
        self.exit=2
        self.exitYes=3
        self.showsetting=4
        self.setsetting=5
        self.prompt=-1
        self.reset=6
        self.adon=7
        self.adoff=8
        self.help=9

        

    def SetInfo(self):
        if self.token=="==Telegram Bot Token==" or self.my_chat_id=="==Telegram Bot ChatID==":
            with open("./telegramKey.txt") as f:
                lines = f.readlines()
                self.token = lines[0].strip()
                self.my_chat_id=lines[1].strip()

        self.URL="https://api.telegram.org/bot{}/".format(self.token)

    def send_message(self,text):
        url = self.URL + "sendMessage?text={}&chat_id={}".format(text, self.my_chat_id)
        self.RequestTelegramBot(url)

    def send_photo(self, photo_path, caption=None):
        url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        files = {'photo': open(photo_path, 'rb')}
        data = {'chat_id': self.my_chat_id, 'caption': caption}
        response = requests.post(url, files=files, data=data)
        return response.json()

    def RequestTelegramBot(self,url):
        response = requests.get(url,verify=False)
        content = response.content.decode("utf8")
        #print("Request Telegram: "+content)
        return content

    def GetUpdates(self):
        url = self.URL + "getUpdates"
        js = self.GetJsonResultFromRequest(url)
        return js

    def GetJsonResultFromRequest(self,url):
        content = self.RequestTelegramBot(url)
        js = json.loads(content)
        return js

    def get_last_chat_id_and_text(self,updates):
        num_updates = len(updates["result"])
        if num_updates<=0:
            return "null","0","0"

        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        message_id=updates["result"][last_update]["message"]["message_id"]
        return (text, chat_id,message_id)

    def CheckMessageInLoop(self):
        time.sleep(1)
        text,chat_id,msg_id = self.get_last_chat_id_and_text(self.GetUpdates())
        
        if msg_id in self.msgSet:
            return (0,"")

        
        if text !="null":
            if "생성" in text:
                self.msgSet.add(msg_id)
                return (self.makeStart,"")
            if "종료" in text:
                self.msgSet.add(msg_id)
                self.exitPlag=True
                return (self.exit,"")
            if "네" in text and self.exitPlag==True:
                self.msgSet.add(msg_id)
                return (self.exitYes,"")
            if "아니오" in text and self.exitPlag==True:
                self.msgSet.add(msg_id)
                self.exitPlag=False
                return (0,"")
            if "?" in text:
                self.msgSet.add(msg_id)
                return (-1,text)
            
            if "=" in text:
                self.msgSet.add(msg_id)
                return (self.setsetting,text)
            
            if "셋팅" in text:
                self.msgSet.add(msg_id)
                return (self.showsetting,"")
            
            if "초기화" in text:
                self.msgSet.add(msg_id)
                return (self.reset,"")
            if "adon" in text:
                self.msgSet.add(msg_id)
                return (self.adon,"")
            if "adoff" in text:
                self.msgSet.add(msg_id)
                return (self.adoff,"")
            if "help" in text or "헬프" in text:
                self.msgSet.add(msg_id)
                return (self.help,"")

            

        return (0,"")

            

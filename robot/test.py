import io
from aip import AipSpeech
import requests
import json
import speech_recognition as sr
import pyttsx3
import RPi.GPIO as GPIO
import sys
import os
import time
import test1 as t
import wave
import pyaudio
from pygame import mixer
import vlc
import mutagen


INT1 = 11
INT2 = 12
INT3 = 13
INT4 = 15


# 2、音频文件转文字：采用百度的语音识别python-SDK
# 导入我们需要的模块名，然后将音频文件发送给出去，返回文字。
# 百度语音识别API配置参数
APP_ID = '24904334'
API_KEY = 'IHusnMqjxU4yRX7yohKzouln'
SECRET_KEY = 'lbIVz6BxGstW5NDlI9omj1FDy5czoKBW'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
path = 'output.wav'

# 3、与机器人对话：调用的是图灵机器人
# 图灵机器人的API_KEY、API_URL
turing_api_key = "fbfb23d8f3714e0dbb91efa89abcae48"
api_url = "http://openapi.tuling123.com/openapi/api/v2"  # 图灵机器人api网址
headers = {'Content-Type': 'application/json;charset=UTF-8'}


# 将语音转文本STT
def listen():
    # 读取录音文件
    with open(path, 'rb') as fp:
        voices = fp.read()
    try:
        # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
        result = client.asr(voices, 'wav', 16000, {'dev_pid': 1536, })
        # result = CLIENT.asr(get_file_content(path), 'wav', 16000, {'lan': 'zh', })
        # print(result)
        # print(result['result'][0])
        # print(result)
        result_text = result["result"][0]
        print("you said: " + result_text)
        return result_text
    except KeyError:
         pass
            



# 图灵机器人回复
def Turing(text_words=""):
    req = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text_words
            },

            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "车公庄"
                }
            }
        },
        "userInfo": {
            "apiKey": turing_api_key,  # 你的图灵机器人apiKey
            "userId": "Nieson"  # 用户唯一标识(随便填, 非密钥)
        }
    }

    req["perception"]["inputText"]["text"] = text_words
    response = requests.request("post", api_url, json=req, headers=headers)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI Robot said: " + result)
    return result

# 调用百度智能云 文字转语音
def voiceChange(text=""):
    print(text)
    result=client.synthesis(text,'zh',1,{
        'vol':5,'per':4,
    })
    if not isinstance(result,dict):
        with open('audio.mp3','wb') as f:
            f.write(result)
    # 调用音频
    os.system('mpg123 audio.mp3')
# def play():
#     
#     mixer.init()
#     mixer.init(frequency=2000,size=16,channels=4)
#     mixer.music.load('audio.mp3')
#     mixer.music.play()
#     
# def play():
#     p=vlc.Mediaplayer("audio.mp3")
#     p.play()   
#    
# 初始化引脚
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INT1,GPIO.OUT)
    GPIO.setup(INT2,GPIO.OUT)
    GPIO.setup(INT3,GPIO.OUT)
    GPIO.setup(INT4,GPIO.OUT)

# 前进代码
def forward():
    GPIO.output(INT1,GPIO.HIGH)
    GPIO.output(INT2,GPIO.LOW)
    GPIO.output(INT3,GPIO.HIGH)
    GPIO.output(INT4,GPIO.LOW)

#后退代码
def back():
    GPIO.output(INT1, GPIO.LOW)
    GPIO.output(INT2, GPIO.HIGH)
    GPIO.output(INT3, GPIO.LOW)
    GPIO.output(INT4, GPIO.HIGH)

#向右后方转弯
def right_back():
    GPIO.output(INT1, GPIO.LOW)
    GPIO.output(INT2, GPIO.HIGH)
    GPIO.output(INT3, GPIO.LOW)
    GPIO.output(INT4, GPIO.LOW)

#向左后放转弯
def Left_forward():
    GPIO.output(INT1, GPIO.HIGH)
    GPIO.output(INT2, GPIO.LOW)
    GPIO.output(INT3, GPIO.LOW)
    GPIO.output(INT4, GPIO.LOW)

#向右前方转弯
def right_forward():
    GPIO.output(INT1, GPIO.LOW)
    GPIO.output(INT2, GPIO.LOW)
    GPIO.output(INT3, GPIO.HIGH)
    GPIO.output(INT4, GPIO.LOW)

#向左后方转弯
def Left_back():
    GPIO.output(INT1, GPIO.LOW)
    GPIO.output(INT2, GPIO.LOW)
    GPIO.output(INT3, GPIO.LOW)
    GPIO.output(INT4, GPIO.HIGH)

#调用回答
def response1():
    # 返回录入音频的内容
    responce=listen()
    # 调用图灵机器人
    request=Turing(responce)

    voiceChange(request)
    


# 对话方法
def talk():
    # 调用这个方法回答"你好"
    voiceChange('您好')   
    while True:
        try:
            voiceChange('你快来和我聊天吧')
            t.record()
            if '前进' in listen():
                    setup()
                    forward()
                    time.sleep(2)
                    GPIO.cleanup()
            elif '后退' in listen():
                    setup()
                    back()
                    time.sleep(2)
                    GPIO.cleanup()
            elif '休息' in listen():
                    return None
        #         elif '左前' in listen():
            #         setup()
            #         Left_forward()
            #         time.sleep(2)
            #         GPIO.cleanup()
            #     elif  '左后' in listen():
            #         setup()
            #         Left_back()
            #         time.sleep(2)
            #         GPIO.cleanup()
            #     elif  '右后' in listen():
            #         setup()
            #         right_back()
            #         time.sleep(2)
            #         GPIO.cleanup()
            #     elif  '右前' in listen():
            #         setup()
            #         right_forward()
            #         time.sleep(2)
            #         GPIO.cleanup()
            else:
                response1()
        except:
            return None
            pass
        continue

def takeup():
    while True:
        t.record()
        if '亚亚' in listen():

# -*- coding:utf-8 -*-

from urllib import urlopen
import urllib
import json
import base64
import pygame
import os
class BaiduRest:
    def __init__(self, cu_id = "test_python", api_key = "SrhYKqzl3SE1URnAEuZ0FKdT" , api_secert = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"):
        # token认证的url
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        # 语音合成的resturl
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        # 语音识别的resturl
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        # 1.获取token
        token_url = self.token_url % (api_key,api_secert)

        r_str = urlopen(token_url).read()
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    def getVoice(self, text, filename):
        # 2. 向Rest接口提交数据
        get_url = self.getvoice_url % (urllib.quote(text), self.cu_id, self.token_str)

        voice_data = urllib.urlopen(get_url).read()
        # 3.处理返回数据
        voice_fp = open(filename,'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        pass

    def playVoice(self,text,filename):
        if not os.path.exists(filename):
            self.getVoice(text,filename)
        pygame.mixer.pre_init(16000, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()


if __name__ == "__main__":
    # 我的api_key,供大家测试用，在实际工程中请换成自己申请的应用的key和secert

    bdr = BaiduRest()
    # 将字符串语音合成并保存为out.mp3
    bdr.playVoice("你好北京邮电大学!", "out.mp3")
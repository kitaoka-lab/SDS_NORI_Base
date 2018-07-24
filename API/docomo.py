#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 各種設定項目 ##################################################
'''
API_KEYは，docomoのAPI利用登録から得られる．
APP_IDは，NORI_Base内の tools/docomo_api_registration.py にAPI_KEYを書き込むことで得られる．
'''

shiritori_flag = False              # True:しりとりモード

APIKEY = '69446d4c53496853524b2f725469645445422e4d5a416d7a525a78424753663363753179786a6852644f41'
APP_ID  = '6bf7739e-ac7c-4996-9dc5-8ebfb0b41c58'

BASE_URL = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue'


NICKNAME        = '良太'
NICKNAME_YOMI   = 'りょうた'
SEX             = '男'
BLOODTYPE       = 'AB'
BIRTHDATE_YEAR  = '1982'
BIRTHDATE_MONTH = '5'
BIRTHDATE_DAY   = '20'
AGE             = '36'
CONSTELLATIONS  = '牡牛座'
PLACE           = '東京'
MODE            = 'dialog'


# モジュール読み込み #############################################
import urllib.request, urllib.parse # urlエンコードや，送信など
import re                           # 検索，置換など
import sys                          # system周りの制御用（exit）
import os                           # ファイルパス取得

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import requests
import json


# option 設定 ##################################################
options = {}
if shiritori_flag: options['mode'] = 'srtr'


# 接続URLなど準備 ###############################################
url     = '{0}?APIKEY={1}'.format(BASE_URL, APIKEY)
headers = {'Content-type': 'application/json'}
data    = {
  "language":"ja-JP",
  "botId":"Chatting",
  "appId":APP_ID,
  "voiceText":'',
  "clientData":{
  "option":{
    "nickname":NICKNAME,
    "nicknameY":NICKNAME_YOMI,
    "sex":SEX,
    "bloodtype":BLOODTYPE,
    "birthdateY":BIRTHDATE_YEAR,
    "birthdateM":BIRTHDATE_MONTH,
    "birthdateD":BIRTHDATE_DAY,
    "age":AGE,
    "constellations":CONSTELLATIONS,
    "place":PLACE,
    "mode":MODE
    }
  },
  "appRecvTime":"2015-05-05 13:30:00",
  "appSendTime":"2015-05-05 13:31:00"
}


# 初期化(APIに接続) ##############################################




# APIへメッセージを送信し，受信したメッセージをパース ###############
def send_and_get(input_message):
    data['voiceText'] = input_message

    try:
        res = requests.post(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("例外args:", e.args)
        return "エラー：対話APIに接続できません"

    res_json = json.loads(res.text)
    return res_json['systemText']['expression']


# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
def main():
    message = ''
    while message != 'バイバイ':
        print('あなた：', file=sys.stderr, end="")
        sys.stderr.flush()
        message = input('')
        resp = send_and_get(message)
        
        print('相手　：', file=sys.stderr, end="")
        sys.stderr.flush()
        print(resp)


#################################################################
# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
if __name__ == '__main__':
    main()

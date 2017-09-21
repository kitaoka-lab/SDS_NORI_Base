#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 各種設定項目 ##################################################
APP_URL = 'https://chatbot-api.userlocal.jp/api/chat?'
APP_KEY = "43d46d5e9406e977f203"

# モジュール読み込み #############################################
import urllib.request, urllib.parse # urlエンコードや，送信など
import re                           # 検索，置換など
import sys                          # system周りの制御用（exit）

# メッセージをAPIに送信 ##########################################
def send_message(input_message):
    params = {
        "key": APP_KEY,
        "message": input_message
    }

    p = urllib.parse.urlencode(params)  # url形式にエンコード
    url = APP_URL + p                   # APIに投げるURLを作成

    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        response = "エラー：対話APIに接続できません"

    return response


# APIからのレスポンスのパース ####################################
def process_response(response):
    body = response.read()
    body = body.decode('utf-8')

    text = re.search('"result":"(.*?)"', body)
    if text != None:
        text = text.group(1)
        
    return text


# APIへメッセージを送信し，受信したメッセージをパース ###############
def send_and_get(input_message):
    response = send_message(input_message)
    received_message = process_response(response)
    return received_message


# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
def main():
    message = ''
    while message != 'バイバイ':
        print('あなた：', file=sys.stderr, end="")
        sys.stderr.flush()
        message = input('')
        resp = send_and_get(message)
        
        print('相手　 : ', file=sys.stderr, end="")
        sys.stderr.flush()
        print(resp)


#################################################################
# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
if __name__ == '__main__':
    main()

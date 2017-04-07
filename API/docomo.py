#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 各種設定項目 ##################################################
APP_KEY = '794d452f6a73305331544a7a5a6768462e74794262526166565167337634345533724d3376487647787544'
shiritori_flag = False              # True:しりとりモード

# モジュール読み込み #############################################
import urllib.request, urllib.parse # urlエンコードや，送信など
import re                           # 検索，置換など
import sys                          # system周りの制御用（exit）
import os                           # ファイルパス取得

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Docomo 対話APIモジュール ---------------
from doco.client import Client


# 初期化(APIに接続) ##############################################
options = {}
if shiritori_flag:
    options['mode'] = 'srtr'

c = Client(apikey= APP_KEY, user=options)


# APIへメッセージを送信し，受信したメッセージをパース ###############
def send_and_get(input_message):
    res = c.send(utt=input_message, apiname="Dialogue")
    return res['utt']


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

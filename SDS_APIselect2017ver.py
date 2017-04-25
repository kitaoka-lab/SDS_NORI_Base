#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
# 雑談対話APIを用いた　音声対話システム

## 情報
元プログラム：北岡研究室　2016年度B4学生
本プログラム：北岡研究室　特任研究員　西村良太　ryota@nishimura.name

開始日：2017年4月6日

## 内容
音声認識により入力された文を，対話WebAPIに投げ，返ってきたテキストを音声合成出力する．

## 特徴
### APIのプラグイン的利用に対応
API ディレクトリに，対話APIのpythonスクリプトを入れると，本プログラムから自動で読み込まれ，利用できるようになる．

#### API pythonスクリプトの仕様
- 以下の関数を用意
    - send_and_get("入力")：ユーザ発話を入力．返り値はシステム出力
- （おまけ的要素）
    - APIスクリプトを単体で起動した場合には，標準入力・標準出力にて，テキストで対話が行えるようにする


'''

# 各種設定項目 ##################################################
OSlist = ["Windows", "Darwin", "Linux"]     # 対応するOSのリスト（platform.system()で得られる値にすること）
INlist = ["julius", "text"]                 # 対応する入力方法のリスト（一つ目がデフォルトになる）
OUTlist = ["jtalk", "text"]                 # 対応する出力方法のリスト（一つ目がデフォルトになる）

JULIUS_HOST = 'localhost'
JULIUS_PORT = 10500

# モジュール読み込み #############################################
from optparse import OptionParser   # オプション解析用
import platform                     # 利用中のOSの名前を読み込む
import sys                          # system周りの制御用
import time                         # sleepを利用する
import glob, os                     # APIのファイル名を取得する
#import importlib                    # モジュールの動的読み込み
#import API                          # APIディレクトリ内の全部のAPIモジュールを，インポートする

# オプション解析 #################################################
def readOption():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage, version="%prog 1.0")
    parser.add_option("-a", "--api", type="string", dest="api", default=APIList[0],
                    help="select dialogue API (" + ', '.join(APIList) + ")", metavar="API")
    parser.add_option("-d", "--debug",
                    action="store_true", dest="debug", default=False,
                    help="print all debug messages")
    parser.add_option("-i", "--input", type="string", dest="input", default=INlist[0],
                    help="select input method (" + ', '.join(INlist) + ")", metavar="InputMethod")
    parser.add_option("-o", "--output", type="string", dest="output", default=OUTlist[0],
                    help="select output method (" + ', '.join(OUTlist) + ")", metavar="OutputMethod")
    parser.add_option("-l", "--led",
                    action="store_true", dest="led", default=False,
                    help="use LED HIKARI agent")
    return parser.parse_args()


# カウントダウン スリープ #########################################
def countdown(t): # in seconds
    print('count down: ', end="")
    for i in range(t,0,-1):
        print(str(i) + " ", end="")
        sys.stdout.flush()
        time.sleep(1)
    print("")


#################################################################
# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
if __name__=="__main__":
    # APIファイルの存在チェック(オプション表示用にリストを作る) %%%%%%%%%%%%%%%%%%%
    APIList = [os.path.basename(r.replace('.py', '')) for r in glob.glob('./API/*.py')]     # APIディレクトリをlsして，パスをファイル名だけにして，リスト化
    APIList.remove('__init__')

    # オプションチェック %%%%%%%%%%%%%%%%%%%%%%%%%%
    (options, args) = readOption()
    
    # API -------------------------------------
    if options.api in APIList:
        print ("API: " + options.api)
    else:
        print ("\n[ERROR] There is no such API (" + options.api + "). Only for (" + ', '.join(APIList) + ").")
        sys.exit()

    # INPUT Method -------------------------------------
    if options.input in INlist:
        print ("Input: " + options.input)
    else:
        print ("\n[ERROR] There is no such INPUT (" + options.input + "). Only for (" + ', '.join(INlist) + ").")
        sys.exit()

    # Output Method -------------------------------------
    if options.output in OUTlist:
        print ("Output: " + options.output)
    else:
        print ("\n[ERROR] There is no such OUTPUT (" + options.output + "). Only for (" + ', '.join(OUTlist) + ").")
        sys.exit()
    
    # debug flag ----------------------------------------
    if options.debug: print ("DEBUG: " + str(options.debug))


    # OSチェック %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if platform.system() in OSlist:
        print ("OS: " + platform.system())
    else:
        print ("\n[ERROR] This program does not support this OS (" + platform.system() + "). Only for (" + ', '.join(OSlist) + ").")
        sys.exit()

    # API 読み込み %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    api_module = __import__('API.' + options.api)             # モジュールの動的インポート

    # 音声認識器(julius)起動 %%%%%%%%%%%%%%%%%%%%%%
    if options.input == "julius":               # input オプションが「julius」に設定されていたら
        from speech import julius               # Juliusモジュール読み込み（サーバ起動など，初期化処理もなされる）
        import socket                           # juliusとのソケット通信用

        # スリープ（1秒毎にカウントダウンを表示）
        print ("Waiting for julius... ", end="")
        countdown(5)

         # TCPクライアントを作成し接続
        print ("Connect to julius server ...  ")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((JULIUS_HOST, JULIUS_PORT))
        except:
            print ('Unalbe to connect julius server ...')  
            exit()
        print ("OK!")

    # 音声合成器(openJTalk)モジュール読み込み %%%%%%%%%%%%
    if options.output == "jtalk":               # input オプションが「julius」に設定されていたら
        from speech import jtalk                # Juliusモジュール読み込み（サーバ起動など，初期化処理もなされる）

    # LED光エージェントモジュール読み込み %%%%%%%%%%%%
    if options.led:
        from LED import LEDcontroller2

    # 対話ループ ##################################
    message = ''
    while 'バイバイ' not in message:
        # ユーザ入力ターン %%%%%%%%%%%%%%%%%%%%%
        print('あなた：', file=sys.stderr, end="")
        sys.stderr.flush()
        if options.input == "text":         # 入力方法が text なら
            message = input('')
        elif options.input == "julius":     # 入力方法が julius なら
            message = julius.julius_output(client)
            print (message)

        # ユーザ入力を，APIに投げる %%%%%%%%%%%%%
        resp_api = eval('api_module.' + options.api + '.send_and_get')(message)

        # LED光エージェントを使う場合には，led_keyも返ってくるので，その処理
        if options.led:
            if options.api == 'test':
                resp = resp_api[0]
                led_key = resp_api[1]
            else:
                resp = resp_api
                led_key = '0'
        else:
            resp = resp_api

        # システム応答表示 %%%%%%%%%%%%%%%%%%%%%
        print('相手　：', file=sys.stderr, end="")
        sys.stderr.flush()
        print(resp)

        # LED光エージェントを光らせる %%%%%%%%%%%
        if options.led:
            LEDcontroller2.LED(led_key)

        # 音声合成器(OpenJTalk)起動 & 再生 %%%%%
        if options.output == "jtalk":
            jtalk.jtalk(resp)

    # 終了処理 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    julius.kill()   #　ちゃんと動かず●●


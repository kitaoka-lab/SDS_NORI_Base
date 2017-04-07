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
OSlist = ["Windows", "MacOS", "Linux"]      # 対応するOSのリスト（platform.system()で得られる値にすること）

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
    parser = OptionParser(usage=usage, version="%prog 0.2")
    parser.add_option("-a", "--api", type="string", dest="api", default=APIList[0],
                    help="select dialogue API (" + ', '.join(APIList) + ")", metavar="API")
    parser.add_option("-d", "--debug",
                    action="store_true", dest="debug", default=False,
                    help="print all debug messages")

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
    APIList.pop()

    # オプションチェック %%%%%%%%%%%%%%%%%%%%%%%%%%
    (options, args) = readOption()
    if options.api: print ("API: " + options.api)
    if options.debug: print ("DEBUG: " + str(options.debug))

    # OSチェック %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if platform.system() in OSlist:
        print ("OS: " + platform.system())
    else:
        print ("\n[ERROR] This program does not support this OS (" + platform.system() + "). Only for (" + ', '.join(OSlist) + ").")
        sys.exit()

    # API 読み込み %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if options.debug:
        print ('API list:')
        for data in APIList:
            print('\t' + data)

    api_module = __import__('API.' + options.api)             # モジュールの動的インポート
    print ("結果：" + eval('api_module.' + options.api + '.send_and_get')("こんにちは"))

    # 音声認識器(julius)起動 %%%%%%%%%%%%%%%%%%%%%%
    # ●●

    # スリープ（1秒毎にカウントダウンを表示）
    print ("Waiting for julius... ", end="")
    countdown(3)

    # 音声合成器(OpenJTalk)起動 %%%%%%%%%%%%%%%%%%%
    # ●●

    # スリープ（1秒毎にカウントダウンを表示）
    print ("Waiting for openJTalk... ", end="")
    countdown(3)

    # 対話ループ ##################################
    # ●●
    # バイバイ で終了


    # ユーザ入力読み込み --------------
    # 　→ 読み込んで表示


    # APIに入力 ----------------------


    # システム出力
    # 　→ 読み込んで表示
    # 　→ 音声合成
    # 対話ループここまで ##########################


    # 最後のシステム発話（バイバイに対する）%%%%%%%%%
    # ●●


    # 終了処理 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



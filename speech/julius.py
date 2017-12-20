#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess                   # スレッド立ち上げ
import sys                          # system周りの制御，ファイルパス取得
import os                           # ファイルパス取得
import platform                     # 利用中のOSの名前を読み込む
import socket                       # juliusとのソケット通信用
import time                         # sleep用
import re                           # 文字列検索用
import signal                       # ctrl+c をつかむため

from datetime import datetime       # 現在時間を取得する

# 各種設定項目 ##################################################
OSlist = ["Windows", "Darwin", "Linux"]     # 対応するOSのリスト（platform.system()で得られる値にすること）

AM_SELECT = 'dnn'                           # 音響モデルの選択 gmm か　dnn
HEADMARGIN = 300	                        # 音声区間開始部のマージン(単位: msec) 結果表示に使うだけ
TAILMARGIN = 400	                        # 音声区間終了部のマージン(単位: msec) 結果表示に使うだけ

DEBUG_FLAG = False                          # デバッグ出力（stderrに詳細認識結果）を出力するか

JULIUS_HOST = 'localhost'                   # juliusのホスト
JULIUS_PORT = 10500                         # juliusのポート

LOG_OPT = ''
LOG_DIR = ''

# 初期化処理 ####################################################
prog_starttime = datetime.now()

# ctrl+c 対応 ##################################################
def handler(signal, frame):
    print('\nCTRL+Cで終了します！')
    kill()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

# OSチェック %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
os_now = platform.system()
if os_now in OSlist:
    print ("Julius OS: " + os_now, file = sys.stderr)
else:
    print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
    sys.exit()

if os_now == 'Windows':
    os_name = 'windows'
    bat_name = 'julius_windows_' + AM_SELECT + '.bat'
elif os_now == 'Darwin':
    os_name = 'osx'
    bat_name = 'julius_osx_' + AM_SELECT + '.sh'
elif os_now == 'Linux':
    os_name = 'linux'
    bat_name = 'julius_linux_' + AM_SELECT + '.sh'
else :
    print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
    sys.exit()


# julius起動(モジュールモード) %%%%%%%%%%%%%%%%%
def startup():
    global bat_name
    global RECORD_FLAG

    print ("julius startup ... ", end="", file = sys.stderr)
    sys.stderr.flush()

    cmd_path = os.path.abspath(os.path.dirname(__file__)) + '/' + bat_name
    if os_now == 'Windows':
        if LOG_OPT:
            cmd = [cmd_path, os.path.abspath(os.path.dirname(__file__)) + '/', LOG_OPT, LOG_DIR]
        else:
            cmd = [cmd_path, os.path.abspath(os.path.dirname(__file__)), ]

    elif os_now == 'Darwin' or os_now == 'Linux':
        if LOG_OPT:
            cmd = [cmd_path + ' ' + os.path.abspath(os.path.dirname(__file__)) + '/ ' + LOG_OPT + ' ' + LOG_DIR]
        else:
            cmd = [cmd_path + ' ' + os.path.abspath(os.path.dirname(__file__))]

    julius_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return julius_proc


# カウントダウン スリープ #########################################
def countdown(t): # in seconds
    print('count down: ', end="")
    for i in range(t,0,-1):
        print(str(i) + " ", end="")
        sys.stdout.flush()
        time.sleep(1)
    print("")


# julius kill ##################################################
def kill():
    print('killing julius server ... ')
    #julius_proc.kill()
    if os_now == 'Windows':
        subprocess.Popen(["taskkill","/im","julius.exe"], shell=True)
    elif os_now == 'Darwin' or os_now == 'Linux':
        subprocess.Popen("pkill julius", stdout=subprocess.PIPE, shell=True)
    print("julius server is killed!")

# julius pause #########################################
def julius_pause(sock):
    sock.send(b'PAUSE\n')

# julius resume #########################################
def julius_resume(sock):
    sock.send(b'RESUME\n')

# julius応答XML → 平文 #########################################
def julius_output(sock):
    while True:
        word_list = ''      # 認識結果の単語のリスト
        classid_list = ''   # 認識結果のクラスIDのリスト
        phone_list = ''     # 認識結果の音素のリスト
        cm_list = ''        # 認識結果の信頼度のリスト

        start_time = ''     # 録音開始時間
        end_time = ''       # 録音終了時間

        et = ''             # 録音開始（ミリ秒，プログラム中で図った時間）
        st = ''             # 録音終了（ミリ秒，プログラム中で図った時間）

        recv_buf = ''       # 受信バッファ
        recv_prev = ''      # <SHYPO が来るまでの履歴


        # 受信バッファに認識結果を入れる %%%%%%%%%%%%
        # （バッファしないと，結果が２回に分かれてやってくるときにバグる）
        # 認識結果開始タグが来るまで待つ ------------
        while not '<SHYPO' in recv_buf:
            recv_prev += recv_buf
            recv_buf = ''.join(sock.recv(4096).decode('utf-8'))
            if re.search('STARTRECOG/', recv_buf):
                st = datetime.now() - prog_starttime
            elif re.search('ENDRECOG/', recv_buf):
                et = datetime.now() - prog_starttime

        prev_lines = recv_prev.split('\n') 
        for line in prev_lines:
            if re.search('STATUS="STARTREC"', line):
                start_time =  re.search('TIME="(.*?)"', line).group(1) 
            elif re.search('STATUS="ENDREC"', line):
                end_time =  re.search('TIME="(.*?)"', line).group(1) 

        # 認識結果終了タグが来るまでバッファする -----
        while not re.search('</SHYPO>', recv_buf):
            recv_buf += ''.join(sock.recv(4096).decode('utf-8'))

        # 得た認識結果（XML）を解析する %%%%%%%%%%%%%
        recv_lines = recv_buf.split('\n') 
        for line in recv_lines:
            if re.search('WHYPO', line):
                word_list +=  re.search('WORD="(.*?)"', line).group(1) + ' '
                classid_list +=  re.search('CLASSID="(.*?)"', line).group(1) + ' '
                phone_list +=  re.search('PHONE="(.*?)"', line).group(1) + ' '
                cm_list +=  re.search('CM="(.*?)"', line).group(1) + ' '

        # 結果の出力（stderr） %%%%%%%%%%%%%%%%%%%%%
        if DEBUG_FLAG:
            print('\n[Julius ASR result]', file = sys.stderr)
            print('WORD\t:' + word_list, file = sys.stderr)
            print('CLASS\t:' + classid_list, file = sys.stderr)
            print('PHONE\t: ' + phone_list, file = sys.stderr)
            print('CM\t:' + cm_list, file = sys.stderr)
            print('', file = sys.stderr)
            sys.stderr.flush()

        # 結果の出力（return） %%%%%%%%%%%%%%%%%%%%%
        return ('%02d:%02d:%02d.%06d'%(st.seconds//3600, (st.seconds//60)%60, st.seconds%60, st.microseconds), '%02d:%02d:%02d.%06d'%(et.seconds//3600, (et.seconds//60)%60, et.seconds%60, et.microseconds), re.sub(' ', '', word_list))


# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
if __name__ == '__main__':
    startup()
    print ("Waiting for julius startup ... ", end="")
    sys.stdout.flush()
    countdown(10)

    # TCPクライアントを作成し接続
    print ("Connect to julius server ...  ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((JULIUS_HOST, JULIUS_PORT))
    except:
        print ('Unalbe to connect julius server ...')  
        exit()
    print ("OK!")

    while True:
        # サーバの応答を受信
        (s, e, output) = julius_output(client)
        print (s + '\t' + e + '\t' + "julius: " + output)


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess                   # スレッド立ち上げ
import sys                          # system周りの制御，ファイルパス取得
import os                           # ファイルパス取得
import platform                     # 利用中のOSの名前を読み込む
import socket                       # juliusとのソケット通信用
import time                         # sleep用
import re                           # 文字列検索用

# 各種設定項目 ##################################################
OSlist = ["Windows", "Darwin", "Linux"]     # 対応するOSのリスト（platform.system()で得られる値にすること）

AM_SELECT = 'dnn'                           # 音響モデルの選択 gmm か　dnn
DEBUG_FLAG = False                          # デバッグ出力（stderrに詳細認識結果）を出力するか

JULIUS_HOST = 'localhost'                   # juliusのホスト
JULIUS_PORT = 10500                         # juliusのポート

# 初期化処理 ####################################################
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
print ("julius startup ... ", end="", file = sys.stderr)
sys.stderr.flush()

cmd_path = os.path.abspath(os.path.dirname(__file__)) + '/' + bat_name
if os_now == 'Windows':
    cmd = [cmd_path, os.path.abspath(os.path.dirname(__file__))]
elif os_now == 'Darwin':
    cmd = [cmd_path + ' ' + os.path.abspath(os.path.dirname(__file__))]
elif os_now == 'Linux':
    cmd = [cmd_path + ' ' + os.path.abspath(os.path.dirname(__file__))]

julius_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)


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
    subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=julius_proc.pid))
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

        recv_buf = ''       # 受信バッファ

        # 受信バッファに認識結果を入れる %%%%%%%%%%%%
        # （バッファしないと，結果が２回に分かれてやってくるときにバグる）
        # 認識結果開始タグが来るまで待つ ------------
        while not '<SHYPO' in recv_buf:
            recv_buf = ''.join(sock.recv(4096).decode('utf-8'))

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
        return re.sub(' ', '', word_list)


# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
if __name__ == '__main__':
    print ("Waiting for julius startup ... ", end="")
    sys.stdout.flush()
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

    while True:
        # サーバの応答を受信
        output = julius_output(client)
        print ("julius: " + output)


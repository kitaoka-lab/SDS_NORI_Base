#!/usr/bin/env python
# -*- coding: utf-8 -*-

# モジュール ################################################
import subprocess
import sys                          # system周りの制御，ファイルパス取得
import os                           # ファイルパス取得
import platform                     # 利用中のOSの名前を読み込む
from datetime import datetime       # ファイル名のために
import time                         # speech_pause (sleep) の為
# 各種設定項目 ##################################################
OSlist = ["Windows", "Darwin", "Linux"]     # 対応するOSのリスト（platform.system()で得られる値にすること）
voice_char = 'mei/mei_normal.htsvoice'      # 声　mei, m100
# voice_char =  'm100/nitech_jp_atr503_m001.htsvoice'

speech_rate = 1.0                   # 話速
speech_pause = 0.0                  # 応答の間

# 初期化処理 ####################################################
prog_starttime = datetime.now()

# OSチェック %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
os_now = platform.system()
if os_now in OSlist:
    print ("openJTalk OS: " + os_now, file = sys.stderr)
else:
    print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
    sys.exit()

if os_now == 'Windows':
    os_name = 'windows'
    bat_name = 'open_jtalk_win.exe'
    dic_name = 'dic_sjis'
    play_name = 'play'
elif os_now == 'Darwin':
    os_name = 'osx'
    bat_name = 'open_jtalk_mac'
    dic_name = 'dic_utf8'
    play_name = 'afplay' 
elif os_now == 'Linux':
    os_name = 'linux'
    bat_name = 'open_jtalk'
    dic_name = 'dic_utf8'
    play_name = 'aplay'
else :
    print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
    sys.exit()

# path設定 %%%%%%%%%%%%%%%%%
dir = os.path.abspath(os.path.dirname(__file__)) + '/openjtalk/' 

LOG_DIR = ''

# openJTalk 本体部 #########################################
def jtalk(t):
    # 設定 %%%%%%%%%%%%%%%%%%%
    if LOG_DIR != '':
        outfilename = LOG_DIR + 'tmp.wav'
    else:
        outfilename = dir + '/tmp/tmp.wav'

    open_jtalk=[dir + 'bin/' + bat_name]
    mech = ['-x', dir + dic_name]
    htsvoice = ['-m', dir + 'voice/' + voice_char]
    speed = ['-r', speech_rate]
    outwav = ['-ow', outfilename]
    trace = ['-ot','trace.txt']
    cmd = open_jtalk + mech + htsvoice + speed + outwav + trace

    # プロセス起動 %%%%%%%%%%%%%
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    # テキストを渡す %%%%%%%%%%%
    if os_name == "windows":
        c.stdin.write(t.encode('sjis'))
    elif os_name == "osx":
        c.stdin.write(t.encode('utf-8'))
    elif os_name == "linux":
        c.stdin.write(t.encode('utf-8'))

    c.stdin.close()
    c.wait()

    # 出力されたwaveファイルを再生 %
    FNULL = open(os.devnull, 'w')
    if os_name == "windows":
        player = os.path.abspath(os.path.dirname(__file__)) + '/' + play_name
    elif os_name == "osx":
        player = play_name
    elif os_name == "linux":
        player = play_name
    else:
        print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
        sys.exit()

    # 「間」の挿入
    time.sleep(speech_pause)

    # 時間計測
    st = datetime.now() - prog_starttime

    # 音声再生
    wavplay = [player, outfilename]
    wr = subprocess.Popen(wavplay, stdout=FNULL, stderr=subprocess.STDOUT)
    wr.wait()

    et = datetime.now() - prog_starttime

    # ファイル名を発話開始時間に変更
    if LOG_DIR != '':
        os.rename(outfilename, LOG_DIR + '%02d%02d%02d_%06d.wav'%(st.seconds//3600, (st.seconds//60)%60, st.seconds%60, st.microseconds) )

    return ('%02d:%02d:%02d.%06d'%(st.seconds//3600, (st.seconds//60)%60, st.seconds%60, st.microseconds), '%02d:%02d:%02d.%06d'%(et.seconds//3600, (et.seconds//60)%60, et.seconds%60, et.microseconds))

if __name__ == '__main__':
    while True:
        print('あなた：', file=sys.stderr, end="")
        sys.stderr.flush()
        message = input('')

        jtalk(message)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 各種設定項目 ##################################################
OSlist = ["Windows", "Darwin", "Linux"]     # 対応するOSのリスト（platform.system()で得られる値にすること）
voice_char = 'mei/mei_normal.htsvoice'      # 声　mei, m100
# voice_char =  'm100/nitech_jp_atr503_m001.htsvoice'

speech_rate = '1.0'                         # 話速

# モジュール ################################################
import subprocess
import sys                          # system周りの制御，ファイルパス取得
import os                           # ファイルパス取得
import platform                     # 利用中のOSの名前を読み込む

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
    dic_name = 'dic_win'
    play_name = 'play'
elif os_now == 'Darwin':
    os_name = 'osx'
    bat_name = 'open_jtalk_mac'
    dic_name = 'dic'
    play_name = 'afplay' 
elif os_now == 'Linux':
    os_name = 'linux'
    bat_name = 'jtalk'
    dic_name = 'dic'
    play_name = 'aplay'
else :
    print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
    sys.exit()

# path設定 %%%%%%%%%%%%%%%%%
dir = os.path.abspath(os.path.dirname(__file__)) + '/openjtalk/' 

# openJTalk 本体部 #########################################
def jtalk(t):
    # 設定 %%%%%%%%%%%%%%%%%%%
    open_jtalk=[dir + 'bin/' + bat_name]
    mech = ['-x', dir + '1.09/' + dic_name]
    htsvoice = ['-m', dir + 'voice/' + voice_char]
    speed = ['-r', speech_rate]
    outwav = ['-ow', dir + 'tmp/open_jtalk.wav']
    cmd = open_jtalk + mech + htsvoice + speed + outwav

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
        player = ""
    else:
        print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
        sys.exit()

    wavplay = [player, dir + 'tmp/open_jtalk.wav']
    wr = subprocess.Popen(wavplay, stdout=FNULL, stderr=subprocess.STDOUT)
    wr.wait()

if __name__ == '__main__':
    while True:
        print('あなた：', file=sys.stderr, end="")
        sys.stderr.flush()
        message = input('')

        jtalk(message)

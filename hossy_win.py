#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 各種設定項目 ##################################################
SDS_NAME = "NORI_Base.py"
LOG = "log.txt"

# モジュール読み込み #############################################
import sys                          # system周りの制御用
import subprocess
import datetime

# initialize ###################################################
enc = "cp932"

# get_lines ####################################################
def get_lines(cmd):
    '''
    :param comd: str 実行コマンド
    :rtype: generator
    :return: 標準出力＆エラー出力（行ごと）
    '''
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        
        if not line and proc.poll() is not None:
            break


#################################################################
# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
if __name__=="__main__":
    f = open(LOG, 'a')
 
    while True: 
        f.write("\n----------------------------------\n")
        f.write("[date]\n")
        now = datetime.datetime.now()
        f.write(now.isoformat() + "\n\n")

  
        for line in get_lines(cmd='python '+SDS_NAME):
            sys.stdout.write(line.decode(enc))
            sys.stdout.flush()

            f.write(line.decode(enc))
            f.flush()

        subprocess.Popen(["taskkill","/im","NORI_Base.py"], shell=True)
        subprocess.Popen(["taskkill","/im","julius.exe"], shell=True)

    f.close()
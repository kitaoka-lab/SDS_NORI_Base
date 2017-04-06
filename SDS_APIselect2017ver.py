#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
雑談対話APIを用いた　音声対話システム

元プログラム：北岡研究室　2016年度B4学生
本プログラム：北岡研究室　特任研究員　西村良太　ryota@nishimura.name

開始日：2017年4月6日
'''

# モジュール読み込み #############################################
from optparse import OptionParser   # オプション解析用
import platform                     # OSの種類を読み込む
import sys                         # system周りの制御用

# オプション解析 #################################################
def readOption():
    usage = "usage: %prog -o [OS type] [options] arg1 arg2"
    parser = OptionParser(usage=usage, version="%prog 0.1")
    parser.add_option("-o", "--os", type="string", dest="ostype",
                    help="select os type (Windows, Linux, Mac)", metavar="OS")
    parser.add_option("-q", "--quiet",
                    action="store_true", dest="verbose", default=False,
                    help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    # エラー処理（オプションが足りなかったらHELP表示）
    if not options.ostype:
        parser.print_help()
        print ("\n[message] you have to choose OS type (ex. -o Windows)\n")

    return (options, args)


#################################################################
# メイン部分（本スクリプトを直接実行した際に実行される部分） #########
if __name__=="__main__":
    # OSチェック ---------------------------------
    OSlist = ["Windows", "MacOS", "Linux"]
    if platform.system() in OSlist:
        print ("OS: " + platform.system())
    else:
        print ("\n[ERROR] This program does not support this OS (" + platform.system() + "). Only for (" + ', '.join(OSlist) + ").")
        sys.exit()


    # オプションチェック --------------------------
    (options, args) = readOption()
    if options.ostype: print ("OS type: " + options.ostype)
    if options.verbose: print ("VERBOSE: " + str(options.verbose))


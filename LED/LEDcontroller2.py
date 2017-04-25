#coding:utf-8

'''
シリアル通信で文字をArduino側に送信
qが押されたら通信を中止するプログラム

●pynputモジュールが必要
$ sudo pip install pynput
'''

import time                     # time.sleep
import serial                   # モジュール名はpyserialだが, importする際はserialである
import serial.tools.list_ports  # シリアルポートによる通信
from getch import getch         # キー入力取得
import platform                 # 利用中のOSの名前を読み込む
import sys                      # 標準エラー出力へ出力するため

# 各種設定 ############################################
OSlist = ["Windows", "Darwin", "Linux"] # 対応するOSのリスト（platform.system()で得られる値にすること）
WAIT = 0.016                            # countによるLED輝度変更時の1ループのwait

# OSチェック %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
os_now = platform.system()
if os_now in OSlist:
  print ('LED OS: ' + os_now + '\n', file = sys.stderr)
else:
  print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
  sys.exit()

if os_now == 'Windows':
  os_name = 'windows'
  SERIAL_PORT = 'COM3'
elif os_now == 'Darwin':
  os_name = 'osx'
  SERIAL_PORT = '/dev/cu.usbmodem1411'
elif os_now == 'Linux':
  os_name = 'linux'
  SERIAL_PORT = '/dev/cu.usbmodem1411'
else :
    print ("\n[ERROR] This program does not support this OS (" + os_now + "). Only for (" + ', '.join(OSlist) + ").", file = sys.stderr)
    sys.exit()

# シリアルポートとの通信開始　#############################
ser = serial.Serial(SERIAL_PORT,9600)

# LEDライト関数 ########################################
def LED(key):
  if key == '1': 
    for count in range(50):
      ser.write(bytes("#7,100,"+str(count)+"\n", 'utf-8'))
      time.sleep(WAIT)

  elif key == '2':
    for count in range(255):
      ser.write(bytes("#7,10,"+str(count)+"\n", 'utf-8'))
      time.sleep(WAIT)

  elif key == '3':
    ser.write(bytes("#3,100,100\n", 'utf-8'))

  elif key == '4':
    ser.write(bytes("#6,0,150,255,255,0,0\n", 'utf-8'))

  elif key == '5':
    ser.write(bytes("#6,0,255,255,255,0,1\n", 'utf-8'))

  elif key == '6':
    ser.write(bytes("#1,30,255,0,128,200\n", 'utf-8'))

  # elif key == '7':

  elif key == '8':
    ser.write(bytes("#4,30,255\n", 'utf-8'))

  elif key == '9':
    ser.write(bytes("#8,30,255\n", 'utf-8'))

  elif key == '0':
    ser.write(bytes("#-1\n", 'utf-8')) 

  elif key == 'a' or key == 'red':
    ser.write(bytes("#2,200,0,0\n", 'utf-8')) 

  elif key == 'b' or key == 'pink':
    ser.write(bytes("#6,0,150,200,50,50,0\n", 'utf-8')) 

  elif key == 'up': 
      ser.write(bytes("#7,100,50\n", 'utf-8'))

  else:
    print('unknown key is pressed!')

  return True



# メイン関数 ############################################
def main():
  # serialポート一覧表示
  print('ポートリスト')
  for i,dev in enumerate(serial.tools.list_ports.comports()):
    print(str(i) + ': ' + dev.device)

  print('')
  # 確認表示
  print('光り方とキーの対応')
  print('- 1：虹色に光る（輝度：50　回転：遅い）')
  print('- 2：虹色に光る（輝度：255　回転：早い）')
  print('- 3：緑色1個が回転（輝度：100　回転：100）')
  print('- 4：黄色に光っていく（輝度：255）')
  print('- 5：光が消える（4の次に押したら，黄色が減衰していく）')
  print('- 6：青と緑がランダム点滅（輝度：255）')
  print('- 7：なし')
  print('- 8：白数個が回転（輝度：255　回転：早め 30）')
  print('- 9：赤がゆっくり明暗（輝度：255 速度：30）')
  print('- 0：消灯')
  print('- a：赤に点灯')
  print('')
  print('Push any key. (q : exit)')

  # 送信部（メインループ）%%%%%%%%%%%%%%%%%%%%%%%%%%%
  while True:      
    # ユーザ入力 -------------------------
    key = getch()

    # qが押されたら終了
    if key == 'q': # q
      ser.write(bytes('#-1\n', 'utf-8'))
      break
    
    # シリアル通信:送信 -------------------------
    LED(key)

  ser.close()

# 単独で，本スクリプトが実行された場合 ##########################
if __name__ == "__main__":
  main()

# LED光エージェント

## 関係者情報
- 作成者：石黒祥生（名古屋大学）ishiguro.yoshio@g.sp.m.is.nagoya-u.ac.jp
- プログラム更新＆ドキュメント作成者：西村良太（徳島大学） ryota@nishimura.name

## LED光エージェントの動作
必要環境をセットアップし，動作させると，接続元PCの数字キー（テンキーでも，フルキーでも動作する）を押すと，対応する動きが行われる．

- 数字キーと動作の対応表
    - 1：虹色に光る（輝度：50　回転：遅い）
    - 2：虹色に光る（輝度：255　回転：早い）
    - 3：緑色1個が回転（輝度：100　回転：100）
    - 4：黄色に光っていく（輝度：255）
    - 5：光が消える（4の次に押したら，黄色が減衰していく）
    - 6：青と緑がランダム点滅（輝度：255）
    - 7：なし
    - 8：白数個が回転（輝度：255　回転：早め 30）
    - 9：赤がゆっくり明暗（輝度：255 速度：30）
    - 0：消灯
- その他の動作
    - マウスクリック：赤に点灯

実際には，操作側PC（Processingプログラム）から，シリアル通信にて信号が発信され，Arduinoがその信号を受け取り，対応する動作（光り方）を行う．

## 使用機器
- 操作用PC（ProcessingがインストールされたPC　OSはなんでも良い）
- LED光エージェント（Arduino DUE基盤に，フルカラーシリアルLEDを接続したもの）
- USBケーブル（Type Aオス - Type Microオス）

## 接続方法
PCのUSBポートににUSBケーブル（TypeA側）を挿し，ArduinoのPROGRAMMING（->ATMEGA16U2）ポートにUSBケーブル（Micro側）を挿す．

## ソフトのインストール
### Arduino用環境＆プログラムの書き込み
#### ダウンロード
Arduinoの最新版（執筆時点では，v1.8.2）を用います．

Arduinoのホーム
https://www.arduino.cc/
から，SOFTWARE
https://www.arduino.cc/en/Main/Software
をたどり，Download the Arduino IDE のところから，自分のOS用の環境をダウンロードしてインストールする．

#### インストール
- ダウンロードしたArduinoIDE をインストール＆起動
- 対応するJavaの環境がない場合には，起動直後に注意されるので，対応するJREをインストール
- Arduinoのライブラリを追加（Adafruit NeoPixel)
    - メニュー：スケッチ → ライブラリをインクルード → ライブラリの管理 → `Adafruit NeoPixel` を検索してインストール

#### Arduinoへのプログラムの書き込み
- PCとArduinoを接続
- ArduinoIDEを起動
    - この時，「ボードArduino Dueを使うにはパッケージをインストールしてください．」と表示されたら，クリックしてインストールする
- ArduinoIDEメニュー：ツール → ボード → ボードマネージャ
    - `DUE` を検索
    - `Arduino SAM Boards (32-bits ARM Cortex-M3) by Arduino`をインストール（執筆時点では，v1.6.11)
- ArduinoIDEメニュー：ツール → ボード → Arduino Due（Programming Port）を選択
- ArduinoIDEメニュー：ツール → ポート → /dev/cu.usbmodem1411 を選択
- ArduinoIDEに，disptestA2.ino を読み込む
- ArduinoIDEのボタン（✓）を押してコンパイルチェック
    - warningが出るが，無視して進む（重大なエラーが出てたらあぶないから，ちゃんと読んで！）
- ArduinoIDEのボタン（→）を押してプログラムをArduinoに書き込む

以下のように出力されれば成功（の可能性がある）

```
スケッチが プログラムストレージ領域の 39,076バイト (7%) を使用しています。最大は 524,288バイト です。
Erase flash
Write 42108 bytes to flash

[                              ] 0% (0/165 pages)
[=                             ] 6% (10/165 pages)
[===                           ] 12% (20/165 pages)
[=====                         ] 18% (30/165 pages)
[=======                       ] 24% (40/165 pages)
[=========                     ] 30% (50/165 pages)
[==========                    ] 36% (60/165 pages)
[============                  ] 42% (70/165 pages)
[==============                ] 48% (80/165 pages)
[================              ] 54% (90/165 pages)
[==================            ] 60% (100/165 pages)
[====================          ] 66% (110/165 pages)
[=====================         ] 72% (120/165 pages)
[=======================       ] 78% (130/165 pages)
[=========================     ] 84% (140/165 pages)
[===========================   ] 90% (150/165 pages)
[============================= ] 96% (160/165 pages)
[==============================] 100% (165/165 pages)
Verify 42108 bytes of flash

[                              ] 0% (0/165 pages)
[=                             ] 6% (10/165 pages)
[===                           ] 12% (20/165 pages)
[=====                         ] 18% (30/165 pages)
[=======                       ] 24% (40/165 pages)
[=========                     ] 30% (50/165 pages)
[==========                    ] 36% (60/165 pages)
[============                  ] 42% (70/165 pages)
[==============                ] 48% (80/165 pages)
[================              ] 54% (90/165 pages)
[==================            ] 60% (100/165 pages)
[====================          ] 66% (110/165 pages)
[=====================         ] 72% (120/165 pages)
[=======================       ] 78% (130/165 pages)
[=========================     ] 84% (140/165 pages)
[===========================   ] 90% (150/165 pages)
[============================= ] 96% (160/165 pages)
[==============================] 100% (165/165 pages)
Verify successful
Set boot flash true
CPU reset.
```

### ProcessingによるArduino制御プログラム実行
#### ダウンロード
Processingは（執筆時点では）最新版のv3.3.1でも動作可能です．

Processingのホーム
https://processing.org/
から，DOWNLOAD
https://processing.org/download/
をたどり，自分のOS用の環境をダウンロードしてインストールする．

#### 準備
- Processingを起動し，LEDcontroller2.pde を読み込む
- 接続するシリアルポートを書き換える（プログラム59行目）
    - `String portName = Serial.list()[3];`
    - 末尾の[3] に入っている数字を変更する．
    - Windowsの場合には，0 にする
    - MacOSの場合には，一度プログラムを実行して表示されるポート一覧を見て入力する
        - 表示例：以下の場合4つのデバイスが表示されているが，0からカウントしていくので，1の場所に「/dev/cu.usbmodem1411 (Arduinoにつながっているポート)」が表示されている．よって，設定は [1] となる．
        - ``` /dev/cu.Bluetooth-Incoming-Port /dev/cu.usbmodem1411 /dev/tty.Bluetooth-Incoming-Port /dev/tty.usbmodem1411 ```

#### 実行
- プログラムを正しく設定し，Processingの再生ボタン（▶）をクリックすれば，実行可能

## 操作方法
テンキーもしくは，フルキーの数字を押す．もしくは，PC上に出現したwindowをマウスでクリックする．


## シリアル通信
PCとArduinoを接続し，ArduinoIDEの ツール → シリアルモニタ を開き，そこから直接Arduinoにシリアル通信で信号を送信することができる．

### 設定
シリアルモニタの設定は以下のようにすること．
- 改行方法：LFのみ
- 通信速度：9600bps

### 送信方法
windowの上のテキストエリアに，送信したいデータを入力して送信する．

### 送信データの例
- `#6,0,150,255,255,0,0`
- `#4,30,255`

最初の`#x`が光り方，その後の数字が，引数的な役割をはたしている．

### 送信するデータの書式
```
消灯
#-1

DIRECTION
ch, speed, intensity, angle
#0,0-1023,0-255,0-360

RANDOM
ch, speed, intensity R G B
#1,0-1023,0-255,0-255,0-255,0-255

COLOR
ch, R, G, B
#2,0-255,0-255,0-255

RADAR
ch speed intensity
#3,0-1023,0-255

CYRCLE
ch speed intensity R, G, B
#4,0-1023,0-255, 0-255, 0-255, 0-255

CYCLE BLUE
ch speed intensity
#5,0-1023,0-255

WARN 
ch speed intensity R G B direction
#6,0-1023,0-255,0-255,0-255,0-255, 0:1

RAINBOW
ch speed intensity
#7,0-1023,0-255

GLOW
ch speed intensity
#8,0-1023,0-255

*speed 0:fastest
```




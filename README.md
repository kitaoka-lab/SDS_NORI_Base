# 雑談対話APIを用いた　音声対話システム
## 情報
元プログラム：北岡研究室　2016年度B4学生

本プログラム：北岡研究室　特任研究員　西村良太　ryota@nishimura.name

開始日：2017年4月6日

## 内容
音声認識により入力された文を，対話WebAPIに投げ，返ってきたテキストを音声合成出力する．

特徴としては，APIのプラグイン的利用に対応しており，API ディレクトリに，対話APIのpythonスクリプトを入れると，本プログラムから自動で読み込まれ，利用できるようになる．

#### API pythonスクリプトの仕様（自分で作りたかったら）
- 以下の関数を用意
    - input("入力")：ユーザ発話を入力．返り値はシステム出力のテキスト
- （docomo, noby, userlocalのおまけ的要素）
    - APIスクリプトを単体で起動した場合には，標準入力・標準出力にて，テキストで対話が行えるようにする

## インストール方法
### 1：ダウンロード
https://github.com/sayonari/SDS_APIselect2017ver から，プログラムをclone or ダウンロード

cloneなら

`$ git clone https://github.com/sayonari/SDS_APIselect2017ver.git`


ダウンロードなら，githubのページからダウンロード（↓リンク）．展開しておく．

https://github.com/sayonari/SDS_APIselect2017ver/archive/master.zip

### 2：juliusとopenJTalkを入れる
juliusはディクテーションキットをダウンロードして展開し，juliusというディレクトリ名で，speechディレクトリ内に入れる．

- ディクテーションキット：http://julius.osdn.jp/index.php?q=dictation-kit.html
    - ダウンロード → zip で入手：https://osdn.net/projects/julius/releases/66544
- ファイルを展開
- ディレクトリ名を「julius」に変更し，speechディレクトリの中に入れる
    - 展開したディレクトリが二重になっていないかチェック

openJTalk は，以下のようなディレクトリ構成になるように，ファイルを用意する．

http://open-jtalk.sourceforge.net/


- openjtalk
    - 1.09
        - bin
        - dic (utf8版）
        - dic_win（shiftjis版）
        - include
        - lib
    - bin（win版，mac版の実行ファイル）
    - tmp（wavファイルがここに生成される）
    - voice（htsvoiceファイル）
        - m100
        - mei

## 実行方法
SDS_APIselect2017ver.pyを実行するだけ．

`$ python3 ./SDS_APIselect2017ver.py`

オプションに対応している．`-h` をつけて起動すると，HELPが表示される．

```
Usage: SDS_APIselect2017ver.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a API, --api=API     select dialogue API (docomo, noby, userlocal)
  -d, --debug           print all debug messages
  -i InputMethod, --input=InputMethod
                        select input method (text, julius)
  -o OutputMethod, --output=OutputMethod
                        select output method (text, jtalk)
```

オプションを付けずに起動すると，テキスト入出力で，APIと対話するモードになる．デフォルトのAPIは，ファイル名順なので「docomo」になる．

## その他
### スクリプトの起動
APIディレクトリ内の，各対話API用pythonスクリプトや，speechディレクトリ内のjulius.py，jtalk.pyは，それぞれ単体で動作する．

API対話スクリプトは，テキストによって標準入出力で対話ができる．juliusは音声認識ができ，jtalkは入力したテキストが読み上げられる．

### API導入方法
APIスクリプトの仕様に合わせて作成したスクリプトを，APIディレクトリに入れるだけで，利用可能になる．オプションでの指定名は，ファイル名そのものになる．



## 注意
docomo　APIを使うときには，以下のモジュールをインストールする必要がある

'''
$ pip install requests
$ pip install simplejson
'''


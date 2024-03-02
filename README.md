# 準備
```shell
$ pip install -r requirements.txt
$ brew install ffmpeg 
```

# 手順
音声ファイルをモノラルのMP3に変換
```shell
$ ffmpeg -i input.m4a -ac 1 -codec:a libmp3lame -q:a 2 output.mp3
```

音声からノイズを除去して、音量を揃える
```shell
$ python main.py input.mp3 output.mp3
```
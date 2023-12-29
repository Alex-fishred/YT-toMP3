import requests
import re
from pytube import Playlist, YouTube
import os
import ssl
from pathlib import Path
ssl._create_default_https_context = ssl._create_stdlib_context

# 觀察後發現所有播放清單網址的差別都在/watch後面，所以須將完整網址拆成兩部分
playlist_url = input('請輸入您要下載的播放清單的網址，例如：https://www.youtube.com/watch?v=U9Z9X_YXaNY&list=PLK6ydMqyKds_8YErvE98g4w690Ofr1GkK&index=1')
playlist = Playlist(playlist_url)

# 以os指定影片下載到哪個資料夾，若不存在此資料夾則建立新資料夾
pathdir = "D:\\YT音樂\\2"
if not os.path.isdir(pathdir):
    os.mkdir(pathdir)

n = 1
for video in playlist:
    yt = YouTube(video)
    print(str(n) + '.' + yt.title)

    # 用 filter 篩選只有音訊的串流，再下載第一個符合條件的影片，並下載到指定資料夾
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(pathdir)

    # 使用 Path 處理檔案名稱，過濾掉無效字元
    base, ext = os.path.splitext(audio_stream.title)
    valid_filename = ''.join(char for char in base if char.isalnum() or char in (' ', '.', '-', '_'))
    new_filename = os.path.join(pathdir, f"{valid_filename}.mp3")
    os.rename(os.path.join(pathdir, audio_stream.default_filename), new_filename)

    n = n + 1

# 所有影片下載完成後，告訴使用者影片下載完成
print('影片下載完成~')

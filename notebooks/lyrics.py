import requests
from bs4 import BeautifulSoup

def get_lyrics(url):
    response = requests.get(url)

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到所有包含歌词的div元素
    lyric_divs = soup.select("div.song-lyrics-line")
    if not lyric_divs:
        return None

    # 提取歌词文本,存入一个列表
    lyrics = []
    for div in lyric_divs:
        # 只提取第一个子div的文本,避免提取翻译
        lyric = div.select_one("div").get_text(strip=True)
        if lyric:  # 跳过空行
            lyrics.append(lyric)

    lyrics = "\n".join(lyrics)
    return lyrics

import pandas as pd
df = pd.read_csv('../datasets/popular_songs.csv')
print(df.head())

import time
from tqdm import tqdm

import csv

# Open the files in append mode
with open('../datasets/popular_songs_with_lyrics.csv', 'a', newline='') as lyrics_file, open("retry.csv", "a", newline='') as retry_file:
    lyrics_writer = csv.writer(lyrics_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    retry_writer = csv.writer(retry_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lyrics_writer.writerow(['song_name', 'rapper', 'url', 'lyrics'])
    retry_writer.writerow(['song_name', 'rapper', 'url'])
    for i, row in tqdm(df.iterrows()):
        url = row['链接']
        try:
            ly = get_lyrics(url)
            print(len(ly))
            assert len(ly) > 0
            # Write the lyrics to the file immediately after fetching
            lyrics_writer.writerow([row['歌名'], row['歌手'], row['链接'], ly])
        except:
            print(f"Error: {url}")
            # Write the retry row to the file immediately after the error
            retry_writer.writerow([row['歌名'], row['歌手'], row['链接']])
        time.sleep(2)
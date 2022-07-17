# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
from collections import deque

# base_url = input('検索したい会社のURLを入力してください: ')
# search_word = input('探したいワードを入力してください: ')
base_url = "https://www.hioki.co.jp/"
search_word = 'HIOKIは、電気設備の工事やメンテナンス作業を、安全かつ効率的に進めていただくことができる製品を提供します。'

# # URL指定
all_urls_allow_duplicate = []
all_urls = {base_url}
matched_urls = []
stack = [base_url]

# stackから取り出して、そのURLのリンクを全て取得する、一軒ずつsetの中に入ってるか確認して、あったら、消す、なかったら、setとstackに入れる、全部仕分けられたら、stackの中身を取り出して再度行う。
i = 0
while stack:
    url = stack.pop(-1)

    i +=1
    print(i)
    print('stack : ',len(stack))
    print('url',url)
    print('-------')
    # time.sleep(1)

    if '.mp4' in url:
        continue

    # Responseオブジェクト生成
    response = requests.get(url)
    # 文字化け防止
    response.encoding = response.apparent_encoding
    # BeautifulSoupオブジェクト生成
    soup = BeautifulSoup(response.text, "html.parser")

    urls_on_this_page = []

    for a_tag in soup.find_all('a'):
        searched_url = a_tag.get('href')
        all_urls_allow_duplicate.append(searched_url)

        if searched_url == base_url:
            continue

        if searched_url == None:
            continue

        # print('base_url: ',base_url,' searched_url: ',searched_url)
        if searched_url.startswith('/'):
            if base_url.endswith('/'):
                searched_url = base_url + searched_url[1:]
            else: 
                searched_url = base_url + searched_url

        if not searched_url.startswith(base_url):
            continue

        if searched_url in all_urls:
            continue
        all_urls.add(searched_url)
        stack.append(searched_url)

    if soup.find('body') == None:
        continue

    if search_word in soup.find('body').text:
        matched_urls.append(url)
        print(url,'\n','\n')

print('--------処理終わり-------')
# print('all_urls_allow_duplicate',all_urls_allow_duplicate)
print('all_urls',all_urls,'\n')
print('matched_urls',matched_urls)




# 取得した情報を書き込む用のファイル
f = open('test.txt', 'w')
# 順にファイルへ書き込み
f.write('検索したワード：'+ search_word +'\n'+'\n')
f.write('⬇️マッチしたURL' +'\n')
for i, url in enumerate(matched_urls):
    f.write(str(i)+ ' : '+ url +'\n')
f.close()
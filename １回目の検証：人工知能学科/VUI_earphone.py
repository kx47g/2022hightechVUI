# -*- coding: utf-8 -*-
#Web検索を行えるライブラリ
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
#文字列から抽出
import re
import sotukenlib as skn

#辞書登録
kiso = {"用途":"","接続":"","ノイズキャンセリング":"","音質":"","操作方法":"","マイク":""}
conference = {"用途":"会議","マイク":"あり"}
gaming = {"用途":"ゲーム","接続":"有線","マイク":"あり"}
music = {"用途":"音楽","ノイズキャンセリング":"あり","音質":"いい","マイク":"なし"}
movie = {"用途":"動画","ノイズキャンセリング":"あり","音質":"いい","マイク":"なし"}

#url = 'https://www.amazon.co.jp/s?k='+text+'&__mk_ja_JP=カタカナ'
#requests.get(url)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
browser.get("http://www.amazon.co.jp/")
# 検索フォームが表示されるまで10秒待つ
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "field-keywords")))

#セリフ
Notext = "認識できませんでした"

#main処理

#スレッドを立ててtkinterの画像表示を開始する
thread1 = skn.threading.Thread(target = skn.show_image)
thread1.start()
# 検索フォームのテキストをクリア
#browser.find_element_by_name("field-keywords").clear()
#イヤホンの検索
skn.talk("お探しの物はなんですか？")
keyword = ""
count = 0
while True:
    try:
        keyword = skn.voiceTOtext()
        if "イヤホン" in keyword:
            keyword = "イヤホン"
            break
        else:
            continue
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            skn.talk("お探しの物はなんですか？たとえば、イヤホン、とおっしゃっていただければお探ししますよ。")

# 検索フォームにキーワードを入力
element.send_keys(keyword)
#イヤホンを検索

# 検索実行
element.send_keys(Keys.RETURN)

link = browser.current_url
print(link)
linkjp = skn.urllib.parse.unquote(link, 'UTF-8')
print(linkjp)
html = skn.requests.get(link)
#このURLが表示される
#https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=N3WMK3PTNQVA&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C192&ref=nb_sb_noss_1
all = re.compile(r'YouTube|ユーチューブ|youtube|YOUTUBE|ようつべ|ヨウツベ|Twitter|TWITTER|ツイッター|twitter|prime|Prime|ぷらいむ|PRIME|プライム|アマプラ|TikTok|TIK|tok|ティックトック|NET|ネットフリックス|Netflix|ネトフリ|音楽|music|ミュージック|スポティファイ|Spotify|music|歌|ゲーム|ゲーミング|switch|音ゲ|PS4|会議| オンライン|meeting| Meeting| MEETING|online| ONLINE|Online|ミーティング|zoom|Zoom|ZOOM|LINE|Line|line|ズーム|ライン|らいん:')

#ここで用途を聞きたい
skn.talk("イヤホンを使って何をしますか")
count = 0
text = ""
add = "絞り込む項目と内容を話してください。"
while True:
    try:
        text = skn.voiceTOtext()
        if bool(all.search(text)):
            break
        else:
            continue
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            skn.talk("イヤホンを使って何をしますか。たとえば、音楽を聞くなら音質のよいものを、オンライン会議で使うならマイクつきの物をお探しします。どれにいたしましょう。")

#用途に合わせて検索してその画面を表示
if "ゲーム" in text or "ゲーミング" in text or "switch" in text or "音ゲ" in text or "PS4" in text:
    print(list(gaming.items()))
    browser.get("https://www.amazon.co.jp/s?k=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=60BPQIG4HV4D&sprefix=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C209&ref=nb_sb_noss_1")
    skn.talk("おんしつ重視のイヤホンですね。他に必要な機能を教えてください")
    print("ワイヤレスやノイズキャンセリング、値段などで分けることができます")
    startflag = True
    count = 0
    while True:
        try:
            text = skn.voiceTOtext()
            if "ワイヤレス" in text  or "無線" in text or "Bluetooth" in text or "ブルートゥース" in text or "wireless" in text or "ワイアレス" in text or "Wireless" in text or "WIRELESS" in text or "bluetooth" in text:
                browser.get("https://www.amazon.co.jp/s?k=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&rh=n%3A4817937051%2Cp_n_feature_twenty_browse-bin%3A10421953051&dc&ds=v1%3ADkZNociqZ%2BAVqk7Uf6eclHMm9NyyvC9K36GXWBQ38fQ&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=60BPQIG4HV4D&qid=1666759991&rnid=10421952051&sprefix=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C209&ref=sr_nr_p_n_feature_twenty_browse-bin_1")
                skn.talk("では買い物をお楽しみください")
                startflag = False
                break
            elif "ノイズキャンセリング" in text or "キャンセル" in text or "ノイキャン" in text or "ANC" in text or "ノイズ" in text or "noise" in text or "Noise" in text or "NOISE" in text:
                browser.get("https://www.amazon.co.jp/s?k=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&rh=n%3A4817937051%2Cp_n_feature_twenty-two_browse-bin%3A10471757051&dc&ds=v1%3Afp7tkKd1Tqmh9duEFGop8wQ1bEdR2AL%2B2moDvgb39cQ&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=60BPQIG4HV4D&qid=1666759991&rnid=10471755051&sprefix=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C209&ref=sr_nr_p_n_feature_twenty-two_browse-bin_2")
                skn.talk("ではお買い物をお楽しみください")
                startflag = False
                break
            elif "安い" in text:
                price = "&s=price-asc-rank"
                browser.get(link + price)#ページ読み込み
                skn.talk("価格の安い順で表示しました。ごらんください")
                startflag = False
                #高い
            elif "高い" in text:
                price = "&s=price-desc-rank"
                browser.get(link + price)#ページ読み込み
                skn.talk("価格の高い順で表示しました。ごらんください")
                startflag = False
                #~円ぐらい
            elif "円以上" in text or "円より高い"in text:
                price_line = int(skn.re.sub(r"\D", "", text))
                price_only = str(price_line)
                if "万円" in text and "0000" in text:
                    price_line = int(str(price_line) + "0000")
                price = "&low-price=" + str(price_line)
                browser.get(link + price)#ページ読み込み
                skn.talk(price_only+ "円以上の商品です。ごらんください")
                startflag = False
            elif "円以下" in text or "円より安い" in text:
                price_line = int(skn.re.sub(r"\D", "", text))
                price_only = str(price_line)
                if "万円" in text and "0000" in text:
                    price_line = int(str(price_line) + "0000")
                price = "&high-price=" + str(price_line)
                browser.get(link + price)#ページ読み込み
                skn.talk(price_only+ "円以下の商品です。ごらんください")
                startflag = False
            elif "万円" in text or "万" in text:
                price_line = str(re.sub(r"\D", "", text)+"0000")
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif "円" in text:
                price_line = str(re.sub(r"\D", "", text))
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif "値段" in text or "価格"in text:
                skn.talk("予算はいくらですか")
                while True:
                    try:
                        text = skn.voiceTOtext()
                        break
                    except:
                        print(Notext)
                        count += 1
                        if count % 2 == 0:
                            skn.talk("予算はいくらですか")
                price = text
                print(price+"以下の商品を表示します")
                if "万円" in text or "万" in text:
                    price_line = str(re.sub(r"\D", "", text)+"0000")
                elif "円" in text:
                    price_line = str(re.sub(r"\D", "", text))
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/s?k=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=60BPQIG4HV4D&sprefix=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C209&ref=nb_sb_noss_1"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif bool(skn.talk_sleep.search(text)):
                startflag = False
            elif startflag == False:
                continue
        except:
            print(Notext)
            count += 1
            if count % 2 == 0 and startflag == True:
                skn.talk("ワイヤレスやノイズキャンセリング、値段などで分けることができます")
        if startflag == False and skn.keyboard.read_key() == "space":
            skn.talk("、はい、他の条件でお調べしましょうか？絞り込む項目と内容を話してください。")
            startflag = True
            
elif "会議" in text or  "オンライン" in text or "meeting" in text or  "Meeting" in text or  "MEETING" in text or "online" in text or  "ONLINE" in text or "Online" in text or "ミーティング" in text or "zoom" in text or "Zoom" in text or "ZOOM" in text or "LINE" in text or "Line" in text or "line" in text or "ズーム" in text or "ライン" in text or "らいん" in text:
    print(list(conference.items()))
    browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3")
    skn.talk("他に必要な機能を教えてください")
    print("ワイヤレスやノイズキャンセリング、値段などで分けることができます")
    startflag = True
    count = 0
    while True:
        try:
            text = skn.voiceTOtext()
            if "ワイヤレス" in text  or "無線" in text or "Bluetooth" in text or "ブルートゥース" in text or "wireless" in text or "ワイアレス" in text or "Wireless" in text or "WIRELESS" in text or "bluetooth" in text:
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A2113278051&dc&ds=v1%3AAHRXWRjv5ikTiYMR9JCG%2BiDvGyW0X5R4l%2FPH1xj0t0s&qid=1666757958&rnid=2113277051&ref=sr_nr_p_n_feature_nine_browse-bin_1")
                skn.talk("ではお買い物をお楽しみください")
                startflag = False
                break
            elif "ノイズキャンセリング" in text or "キャンセル" in text or "ノイキャン" in text or "ANC" in text or "ノイズ" in text or "noise" in text or "Noise" in text or "NOISE" in text:
                browser.get("https://www.amazon.co.jp/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&i=electronics&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A2113280051&dc&qid=1666758716&rnid=2113277051&ref=sr_nr_p_n_feature_nine_browse-bin_2&ds=v1%3AxZbBcQOB8mKEx6U96IwYbHtk6yoq7HotRTnjsoTUzsY")
                skn.talk("ではお買い物をお楽しみください")
                startflag = False
                break
            elif "音質" in text:
                browser.get("https://www.amazon.co.jp/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A3937867051&dc&ds=v1%3APU8LUuWZCEAWbrRjc7SBK%2BxZjwtcYf4ZgM0hNaBnum0&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=38SXSCL6BIFKB&qid=1666758902&rnid=2113277051&sprefix=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C193&ref=sr_nr_p_n_feature_nine_browse-bin_9")
                skn.talk("ではお買い物をお楽しみください")
                startflag = False
                break
            elif "安い" in text:
                price = "&s=price-asc-rank"
                browser.get(link + price)#ページ読み込み
                skn.talk("価格の安い順で表示しました。ごらんください")
                startflag = False
                #高い
            elif "高い" in text:#元のシナリオには価格で分ける機能は無い。消しとこうかな。
                price = "&s=price-desc-rank"
                browser.get(link + price)#ページ読み込み
                skn.talk("価格の高い順で表示しました。ごらんください")
                startflag = False
                #~円ぐらい
            elif "円以上" in text or "円より高い"in text:
                price_line = int(skn.re.sub(r"\D", "", text))
                price_only = str(price_line)
                if "万円" in text and "0000" in text:
                    price_line = int(str(price_line) + "0000")
                price = "&low-price=" + str(price_line)
                browser.get(link + price)#ページ読み込み
                skn.talk(price_only+ "円以上の商品です。ごらんください")
                startflag = False
            elif "円以下" in text or "円より安い" in text:
                price_line = int(skn.re.sub(r"\D", "", text))
                price_only = str(price_line)
                if "万円" in text and "0000" in text:
                    price_line = int(str(price_line) + "0000")
                price = "&high-price=" + str(price_line)
                browser.get(link + price)#ページ読み込み
                skn.talk(price_only+ "円以下の商品です。ごらんください")
                startflag = False
            elif "万円" in text or "万" in text:
                price_line = str(re.sub(r"\D", "", text)+"0000")
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif "円" in text:
                price_line = str(re.sub(r"\D", "", text))
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif "値段" in text or "価格"in text:
                skn.talk("予算はいくらですか")
                while True:
                    try:
                        text = skn.voiceTOtext()
                        break
                    except:
                        print(Notext)
                        count += 1
                        if count % 2 == 0:
                            skn.talk("予算はいくらですか")
                price = text
                print(price+"以下の商品を表示します")
                if "万円" in text or "万" in text:
                    price_line = str(re.sub(r"\D", "", text)+"0000")
                elif "円" in text:
                    price_line = str(re.sub(r"\D", "", text))
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif bool(skn.talk_sleep.search(text)):
                startflag = False
            elif startflag == False:
                continue
        except:
            print(Notext)
            count += 1
            if count % 2 == 0 and startflag == True:
                skn.talk("ワイヤレスやノイズキャンセリング、値段などで分けることができます")
        if startflag == False and skn.keyboard.read_key() == "space":
            skn.talk("、はい、他の条件でお調べしましょうか？絞り込む項目と内容を話してください。")
            startflag = True

elif "音楽" in text or "music" in text or "ミュージック" in text or "スポティファイ" in text or "Spotify" in text or "music" in text or "歌" in text:
    print(list(music.items()))
    browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=nb_sb_noss_1")
    skn.talk("おんしつ重視のイヤホンですね、ノイズキャンセリングなど他に必要な機能を教えてください")
    startflag = True
    count = 0
    while True:
        count = 0
        try:
            text = skn.voiceTOtext()
            if "ワイヤレス" in text  or "無線" in text or "Bluetooth" in text or "ブルートゥース" in text or "wireless" in text or "ワイアレス" in text or "Wireless" in text or "WIRELESS" in text or "bluetooth" in text:
                browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A2113278051&dc&ds=v1%3AEz%2Fox9QDtpEJttVvBoI%2FrzEieGgY2IvW%2FT9d2MrRApk&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&qid=1666766808&rnid=2113277051&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=sr_nr_p_n_feature_nine_browse-bin_1")
                skn.talk("では買い物をお楽しみください")
                break
            elif "ノイズキャンセリング" in text or "キャンセル" in text or "ノイキャン" in text or "ANC" in text or "ノイズ" in text or "noise" in text or "Noise" in text or "NOISE" in text:
                browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A2113280051&dc&ds=v1%3A2mf5qniqsQ0yN%2FvFn30OnL%2BIJKMVgqH2iI27QuKzzJk&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&qid=1666766808&rnid=2113277051&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=sr_nr_p_n_feature_nine_browse-bin_2")
                skn.talk("ではお買い物をお楽しみください")
                break
            elif "安い" in text:
                price = "&s=price-asc-rank"
                browser.get(link + price)#ページ読み込み
                skn.talk("価格の安い順で表示しました。ごらんください")
                startflag = False
                #高い
            elif "高い" in text:
                price = "&s=price-desc-rank"
                browser.get(link + price)#ページ読み込み
                skn.talk("価格の高い順で表示しました。ごらんください")
                startflag = False
                #~円ぐらい
            elif "円以上" in text or "円より高い"in text:
                price_line = int(skn.re.sub(r"\D", "", text))
                price_only = str(price_line)
                if "万円" in text and "0000" in text:
                    price_line = int(str(price_line) + "0000")
                price = "&low-price=" + str(price_line)
                browser.get(link + price)#ページ読み込み
                skn.talk(price_only+ "円以上の商品です。ごらんください")
                startflag = False
            elif "円以下" in text or "円より安い" in text:
                price_line = int(skn.re.sub(r"\D", "", text))
                price_only = str(price_line)
                if "万円" in text and "0000" in text:
                    price_line = int(str(price_line) + "0000")
                price = "&high-price=" + str(price_line)
                browser.get(link + price)#ページ読み込み
                skn.talk(price_only+ "円以下の商品です。ごらんください")
                startflag = False
            elif "万円" in text or "万" in text:
                price_line = str(re.sub(r"\D", "", text)+"0000")
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif "円" in text:
                price_line = str(re.sub(r"\D", "", text))
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif "値段" in text or "価格"in text:
                skn.talk("予算はいくらですか")
                while True:
                    try:
                        text = skn.voiceTOtext()
                        break
                    except:
                        print(Notext)
                        count += 1
                        if count % 2 == 0:
                            skn.talk("予算はいくらですか")
                price = text
                if "万円" in text or "万" in text:
                    price_line = str(re.sub(r"\D", "", text)+"0000")
                elif "円" in text:
                    price_line = str(re.sub(r"\D", "", text))
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=nb_sb_noss_1"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
            elif bool(skn.talk_sleep.search(text)):
                startflag = False
            elif startflag == False:
                continue
        except:
            print(Notext)
            count += 1
            if count % 2 == 0 and startflag == True:
                skn.talk("ワイヤレスやノイズキャンセリング、値段などで分けることができます")
        if startflag == False and skn.keyboard.read_key() == "space":
            skn.talk("、はい、他の条件でお調べしましょうか？絞り込む項目と内容を話してください。")
            startflag = True
elif "YouTube" in text or "ユーチューブ" in text or "youtube" in text or "YOUTUBE" in text or "ようつべ" in text or "ヨウツベ" in text or "Twitter" in text or "TWITTER" in text or "ツイッター" in text or "twitter" in text or "prime" in text or "Prime" in text or "ぷらいむ" in text or "PRIME" in text or "プライム" in text  or "アマプラ" in text or "TikTok" in text or "TIK" in text  or "tok" in text or "ティックトック" in text or "NET" in text or "ネットフリックス" in text or "Netflix" in text or "ネトフリ" in text:
    print(list(movie.items()))
    browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=nb_sb_noss_1")
    skn.talk("動画を見るときに使うイヤホンですね、他に必要な機能を教えてください")
    startflag = True
    while True:
        count = 0
        try:
            text = skn.voiceTOtext()
            if "ワイヤレス" in text  or "無線" in text or "Bluetooth" in text or "ブルートゥース" in text or "wireless" in text or "ワイアレス" in text or "Wireless" in text or "WIRELESS" in text or "bluetooth" in text:
                browser.get("")
                skn.talk("では買い物をお楽しみください")
                break
            elif "ノイズキャンセリング" in text or "キャンセル" in text or "ノイキャン" in text or "ANC" in text or "ノイズ" in text or "noise" in text or "Noise" in text or "NOISE" in text:
                browser.get("")
                skn.talk("ではお買い物をお楽しみください")
                break
            elif "安い" in text:
                price = "&s=price-asc-rank"
                browser.get(link + price)#ページ読み込み
                skn.talk("価格の安い順で表示しました。ごらんください")
                startflag = False
                #高い
            elif "高い" in text:
                price = "&s=price-desc-rank"
                browser.get(link + price)#ページ読み込み
                skn.talk("価格の高い順で表示しました。ごらんください")
                startflag = False
                #~円ぐらい
            elif "円以上" in text or "円より高い"in text:
                price_line = int(skn.re.sub(r"\D", "", text))
                price_only = str(price_line)
                if "万円" in text and "0000" in text:
                    price_line = int(str(price_line) + "0000")
                price = "&low-price=" + str(price_line)
                browser.get(link + price)#ページ読み込み
                skn.talk(price_only+ "円以上の商品です。ごらんください")
                startflag = False
            elif "円以下" in text or "円より安い" in text:
                price_line = int(skn.re.sub(r"\D", "", text))
                price_only = str(price_line)
                if "万円" in text and "0000" in text:
                    price_line = int(str(price_line) + "0000")
                price = "&high-price=" + str(price_line)
                browser.get(link + price)#ページ読み込み
                skn.talk(price_only+ "円以下の商品です。ごらんください")
                startflag = False
            elif "万円" in text or "万" in text:
                price_line = str(re.sub(r"\D", "", text)+"0000")
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif "円" in text:
                price_line = str(re.sub(r"\D", "", text))
                price_int = "&rh=p_36%3A-" + price_line
                browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
                skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                startflag = False
            elif "値段" in text or "価格"in text:
                skn.talk("予算はいくらですか")
                while True:
                    count = 0
                    try:
                        text = skn.voiceTOtext()
                    except:
                        print(Notext)
                        count += 1
                        if count % 2 == 0 and startflag == True:
                            skn.talk("ワイヤレスやノイズキャンセリング、値段などで分けることができます")
                    price = text
                    print(price+"以下の商品を表示します")
                    if "万円" in text or "万" in text:
                        price_line = str(re.sub(r"\D", "", text)+"0000")
                    elif "円" in text:
                        price_line = str(re.sub(r"\D", "", text))
                    price_int = "&rh=p_36%3A-" + price_line
                    browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=nb_sb_noss_1"+ price_int)#ページ読み込み
                    skn.talk(price_line+ "円付近商品のみ表示しました。他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。")
                    startflag = False
            elif bool(skn.talk_sleep.search(text)):
                startflag = False
            elif startflag == False:
                continue
        except:
            print(Notext)
            count += 1
            if count % 2 == 0 and startflag == True:
                skn.talk("ワイヤレスやノイズキャンセリング、値段などで分けることができます")
        if startflag == False and skn.keyboard.read_key() == "space":
            skn.talk("、はい、他の条件でお調べしましょうか？" + add)
            add = ""
            startflag = True
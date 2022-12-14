# -*- coding: utf-8 -*-
#音声処理用ライブラリ
import sotukenlib as skn

value = 2
double_continue = False
firstflag = True

#喋るための準備
r = skn.sr.Recognizer()
driver_path = "C:\\driver\\chromedriver.exe"
AmazonUrl = 'https://www.amazon.co.jp/'

options = skn.webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = skn.webdriver.Chrome(options=options)
browser.get("http://www.amazon.co.jp/")
element = skn.WebDriverWait(browser, 10).until(skn.EC.presence_of_element_located((skn.By.NAME, "field-keywords")))
chocoUrl = "https://www.amazon.co.jp/s?bbn=2424488051&rh=n%3A2424488051%2Cp_n_feature_"

#スレッドを立ててtkinterの画像表示を開始する
thread1 = skn.threading.Thread(target = skn.show_image)
thread1.start()

departlist = []#カテゴリ一覧
refinelist = []#ブランド一覧
filltername = []#フィルタ一覧
fillterUrl = []#フィルタごとの遷移URL
tastelist = ["ココナッツ","カカオ","グリーンティー","オレンジ","アーモンド","チョコレート","キャラメル"]
#お菓子VUIの画像
imgokasi = skn.Image.open('chocoimage.jpg')
imgokasi = skn.ImageTk.PhotoImage(imgokasi)

#セリフ
rooptext = "他の条件で調べたいときは、スペースキーを押してわたしを呼んでください。"

#talk("価格やブランド、接続方式と、重視するポイントが決まっていれば教えてください。")
linkjp = ""
link = ""
price = ""
brand = ""
order = ""
endflag = False
okasitext = "、お探しの物はなんですか？"
add = "たとえば、チョコレートのお菓子、のようにおっしゃっていただければお探ししますよ"
skn.talk(okasitext)
count = 0
while True:
    skn.voice_recoad()
    with skn.sr.AudioFile("output.wav") as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='ja-JP')
        print(text)
        if "板チョコ" in text:
            link = "https://www.amazon.co.jp/b/?node=2424488051&ref_=Oct_d_odnav_d_71315051_0&pd_rd_w=Tpv7q&content-id=amzn1.sym.ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_p=ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_r=X6M1RTVEDDDVX54BK8J4&pd_rd_wg=3JM2Z&pd_rd_r=19284c33-bf16-4b96-b631-d4c9872d178f"
            browser.get(link)
            skn.canvas.itemconfig(skn.item,image = imgokasi)
            break
        elif "チョコ" in text:
            link = "https://www.amazon.co.jp/b/?node=71315051&ref_=Oct_d_odnav_d_71314051_2&pd_rd_w=kJRPK&content-id=amzn1.sym.ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_p=ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_r=P7EVYQEV135BG4CEYTC3&pd_rd_wg=juDNh&pd_rd_r=d7366d85-ec2a-482a-83d9-1c551e0ef8a5"
            browser.get(link)
            skn.canvas.itemconfig(skn.item,image = imgokasi)
            okasitext = "いろんな種類があります、どのチョコレート菓子にしますか？"
            add = "たとえば、板チョコがいい、のようにおっしゃっていください"
            skn.talk(okasitext)
        elif "お菓子" in text:
            link = "https://www.amazon.co.jp/b/?node=71314051&ref_=Oct_d_odnav_d_57239051_3&pd_rd_w=5lqwu&content-id=amzn1.sym.ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_p=ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_r=0PM6RE9D1XENNAKCVPEZ&pd_rd_wg=rDvy0&pd_rd_r=f65588eb-641a-49cd-8368-17d26d4f0908#section:~:text=Next%20page-,%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA%E3%83%BC%E3%81%8B%E3%82%89%E6%8E%A2%E3%81%99,-%E3%82%B9%E3%83%8A%E3%83%83%E3%82%AF%E8%8F%93%E5%AD%90"
            browser.get(link)
            skn.canvas.itemconfig(skn.item,image = imgokasi)
            okasitext = "駄菓子やスナック、チョコなどがあります。気になるものを選んでください。"
            add = ""
            skn.talk(okasitext)
    except:
        print("認識できませんでした")
        count += 1
        if count % 2 == 0:
            skn.talk(okasitext+add)

#絞り込み台詞
choicetext = "メーカーや価格、味などで絞り込めます。絞り込む項目と内容を話してください。"
skn.talk(choicetext)
choicetext = 'メーカーや価格、味などで絞り込めます。たとえば、アーモンドチョコで検索、のようにおっしゃってください'
#ループ３
count = 0
startflag = True
add = "絞り込む項目と内容を話してください。"
while True:
    try:
        text = skn.voiceTOtext()
        print(text)
        #安い
        if "安い" in text:
            price = "&s=price-asc-rank"
            browser.get(link + price)#ページ読み込み
            skn.talk("価格の安い順で表示しました。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
            #高い
        elif "高い" in text:
            price = "&s=price-desc-rank"
            browser.get(link + price)#ページ読み込み
            skn.talk("価格の高い順で表示しました。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
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
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "円以下" in text or "円より安い" in text:
            price_line = int(skn.re.sub(r"\D", "", text))
            price_only = str(price_line)
            if "万円" in text and "0000" in text:
                price_line = int(str(price_line) + "0000")
            price = "&high-price=" + str(price_line)
            browser.get(link + price)#ページ読み込み
            skn.talk(price_only+ "円以下の商品です。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "円" in text:
            price_line = int(skn.re.sub(r"\D", "", text))
            price_only = str(price_line)
            if "万円" in text and "0000" in text:
                price_line = int(str(price_line) + "0000")
            price_line = str(price_line*0.9) + "-"  + str(price_line*1.1)
            price = "&price=" + price_line
            browser.get(link + price)#ページ読み込み
            skn.talk(price_only+ "円付近の商品です。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
                #価格で絞り込む
        elif "価格" in text:
            choicetext = "価格の安い順、高い順、具体的な価格は決まっていますか？"
            skn.talk(choicetext)
        #チョコレートタイプで絞り込む
        elif "ホワイト" in text or "白い" in text or "甘い" in text:
            TypeUrl = "two_browse-bin%3A10511140051&dc&qid=1666240598&rnid=10511138051&ref=lp_2424488051_nr_p_n_feature_two_browse-bin_0"
            link = chocoUrl + TypeUrl
            browser.get(link + price)
            skn.talk("ホワイトチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "ミルク" in text or "茶色の" in text:
            TypeURL = "two_browse-bin%3A10511139051&dc&qid=1666240325&rnid=10511138051&ref=lp_2424488051_nr_p_n_feature_two_browse-bin_1"
            link = chocoUrl + TypeUrl
            browser.get(link + price)
            skn.talk("ミルクチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "ダーク" in text or "黒い" in text or "ビター" in text or "苦" in text:
            TypeUrl = "two_browse-bin%3A10511141051&dc&qid=1666240325&rnid=10511138051&ref=lp_2424488051_nr_p_n_feature_two_browse-bin_2"
            link = chocoUrl + TypeUrl
            browser.get(link + price)
            skn.talk("ビターチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        #メーカーで絞り込む
        elif "ロッテ" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3A%E3%83%AD%E3%83%83%E3%83%86&dc&qid=1666241034&rnid=2321255051&ref=lp_2424488051_nr_p_89_1"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            skn.talk("ロッテから出ているチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "キャドバリー" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3Aキャドバリー&dc&qid=1666240666&rnid=2321255051&ref=lp_2424488051_nr_p_89_2"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            skn.talk("キャドバリーから出ているチョコです。ごらんください")
            skn.talk(rooptext)
            startflag = False
        elif "ブルボン" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3Aブルボン&dc&qid=1666240666&rnid=2321255051&ref=lp_2424488051_nr_p_89_3"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            skn.talk("ブルボンから出ているチョコです。ごらんください")
            skn.talk(rooptext)
            startflag = False
        elif "リンツ" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3ALindt%28リンツ%29&dc&qid=1666240666&rnid=2321255051&ref=lp_2424488051_nr_p_89_4"
            link = AmazonUrl + MakerUrl
            skn.talk("リンツから出ているチョコです。ごらんください")
            browser.get(link)
            skn.talk(rooptext)
            startflag = False
        elif "明治" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3A明治&dc&ds=v1%3ArUM%2B7edKfR3VRj3ivDsU2FC3KW9lTQNrzpI4eb76hyY&qid=1666242010&rnid=2321255051&ref=sr_nr_p_89_1"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            skn.talk("明治から出ているチョコです。ごらんください")
            skn.talk(rooptext)
            startflag = False
        elif "森永" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3A森永製菓&dc&qid=1666242210&rnid=2321255051&ref=sr_nr_p_89_1&ds=v1%3AU0UBz3RNOnv2o9HdiQENlsIyGnmkCDOleDU%2B8KswzUs"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            skn.talk("森永から出ているチョコです。ごらんください")
            skn.talk(rooptext)
            startflag = False
        #味で絞り込む
        elif "ココナッツ" in text:
            tasteUrl = "five_browse-bin%3A10552923051&dc&qid=1666160411&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_0"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            skn.talk("ココナッツ風味のチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "カカオ" in text:
            print("カカオ")
            tasteUrl = "five_browse-bin%3A10552934051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_1"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            skn.talk("カカオ風味のチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "グリーンティ" in text:
            tasteUrl = "five_browse-bin%3A10552924051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_2"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            skn.talk("グリーンティ風味のチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "オレンジ" in text:
            tasteUrl = "five_browse-bin%3A10552889051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_3"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            skn.talk("オレンジ風味のチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "アーモンド" in text:
            tasteUrl = "five_browse-bin%3A10552898051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_4"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            skn.talk("アーモンド風味のチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "キャラメル" in text:
            tasteUrl = "five_browse-bin%3A10552946051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_6"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            skn.talk("キャラメルチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif "味" in text:
            skn.talk("ココナッツ、カカオ、グリーンティなどの種類があります。どれにいたしましょう。")
        elif "メーカー" in text:
            skn.talk("ロッテや明治などがチョコをだしています、どのメーカーにいたしましょう。")
        elif "チョコ" in text:
            tasteUrl = "five_browse-bin%3A10552915051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_5"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            skn.talk("プレーンな味のチョコです。ごらんください")
            skn.talk(rooptext)
            rooptext = ""
            startflag = False
        elif bool(skn.talk_sleep.search(text)):
            startflag = False
        elif startflag == False:
            continue
    except:
        print("認識できませんでした")
        count += 1
        if count % 2 == 0 and startflag == True:
            skn.talk(choicetext)
    if startflag == False and skn.keyboard.read_key() == "space":
        skn.talk("、はい、他の条件でお調べしましょうか？" + add)
        add = ""
        startflag = True

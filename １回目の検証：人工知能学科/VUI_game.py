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
import webbrowser #VUI_game.py限定ライブラリ
#文字列から抽出
import re
import sotukenlib as skn
import win32com.client
import wave
import pyaudio

#制御用変数
double_continue = False
firstflag = True
endflag = False
soloflag = False
genreflag = ""
reguflag = ""
samplename = ""
glflag = False

#最終的に紹介するゲームソフト
gamelist = []

#条件分岐
#括弧の中のいずれかのワードが喋られた場合,各関数のif文が反応します。

PCpattern = re.compile(r'PC|パソコン|ゲーミング')
SWpattern = re.compile(r'ニンテンドースイッチ|スイッチ|switch|SWITCH')
PSpattern = re.compile(r'プレイステーション|プレステ|PlayStation|PS')


#変数名のPはポジティブ、Nはネガティブの意です。
PSolopattern = re.compile(r'好き|ソロ|一人|はい|うん|そう|せや')
Npattern = re.compile(r'対戦|協力|じゃない|じゃあない|ではない|いや|嫌|困る|苦手|嫌い')

#ジャンルごとのソフト一覧
RPG2 = re.compile(r'PokémonLEGENDSアルセウス|ポケモンアルセウス|アルセウス|ポケモン')
RPG3 = re.compile(r'ドラゴンクエストXI過ぎ去りし時を求めてS|ドラゴンクエスト11|ドラクエ11|ドラゴンクエストイレブン|ドラクエイレブン')
RPG4 = re.compile(r'XenobladeDefinitiveEdition|ゼノブレイド|ゼノブレ')
RPG = re.compile(r'ドラゴンクエストX目覚めし五つの種族オフライン|ドラゴンクエスト10オフライン|ドラクエ10オフライン|ドラクエ10|ドラクエテン')
ACT = re.compile(r'鬼滅の刃ヒノカミ血風譚|鬼滅の刃|きめつ|キメツ')
ACT2 = re.compile(r'星のカービィ ディスカバリー|カービィ ディスカバリー|ディスカバリー|星のカービィ|カービィ')
ACT3 = re.compile(r'モンスターハンターライズ：サンブレイク|モンハンライズ サンブレイク|サンブレイク|モンハンライズ')
ACT4 = re.compile(r'MarvelsSpider-Man:MilesMorales|マーベルスパイダーマン|スパイダーマン')
ACT5 = re.compile(r'クラッシュ・バンディングー4とんでもマルチバース|クラッシュ・バンディグ|バンディグ|バンディク')
ACT6 = re.compile(r'Detroit Become Human|デトロイト ビカム ヒューマン|デトロイト')
LACT = re.compile(r'初音ミクProjectDIVAFutureToneDX|プロジェクトディーヴァ|初音ミク')
ACTRPG = re.compile(r'ドラゴンボールZKAKAROT|ドラゴンボール')
ACTRPG2 = re.compile(r'ペルソナ5スクランブルザファントムストライカーズ|ペルソナ5スクランブル|ペルソナファイブスクランブル|ペルソナ')
AD = re.compile(r'十三機兵防衛圏|十三|防衛兼')
AD2 = re.compile(r'ペーパーマリオオリガミキング|オリガミキング|ペーパーマリオ')
SHUM = re.compile(r'あつまれどうぶつの森|あつ森')
SHUM2 = re.compile(r'StardewValley|スターデューバレー|スタードゥバレー|スターデュ|スタードゥ')
SHUM3 = re.compile(r'ファイアーエムブレム 風花雪月|風花雪月|ファイアーエムブレム')
SHUT = re.compile(r'スプラトゥーン3|Splatoon 3|スプラ3')
SHUT2 = re.compile(r'apex|エーペックス|エイベックス|エペ|えぺ')
OPW = re.compile(r'ゼルダの伝説ブレスオブザワイルド|ゼルダ')
HOL = re.compile(r'Deadby Day light|デッドバイデイライト|dbd')
HOL2 = re.compile(r'リトルナイトメア2|リトルナイトメア')
HOL3 = re.compile(r'バイオハザード ヴィレッジ|バイオ|バイオハザード')
FIT = re.compile(r'リングフィットアドベンチャー|リングフィット|リング')
FIT2 = re.compile(r'FitBoxing2|フィットボクシング|ボクシング')
SPO = re.compile(r'Nintendo Switch Sports|ニンテンドースイッチスポーツ|スイッチスポーツ')
SPO2 = re.compile(r'eBASEBALLパワフルプロ野球2022|イーベースボール|パワプロ')
RA = re.compile(r'マリオカート8デラックス|マリカー|マリカ')
YACT = re.compile(r'夜廻三|夜回りさん|よまわりさん')
#喋るための準備
r = skn.sr.Recognizer()

#関数
#音声録音
def voice_recoad():
    rec_time = 10            # 録音時間[s]
    file_path = "output.wav" #音声を保存するファイル名
    fmt = pyaudio.paInt16  # 音声のフォーマット
    ch = 1              # チャンネル1(モノラル)
    sampling_rate = 44100 # サンプリング周波数
    chunk = 2**11       # チャンク（データ点数）
    audio = pyaudio.PyAudio()
    index = 1 # 録音デバイスのインデックス番号（デフォルト1）

    stream = audio.open(format=fmt, channels=ch, rate=sampling_rate, input=True,
                        input_device_index = index,
                        frames_per_buffer=chunk)
    print("聞き取っています...")
    # 録音処理
    frames = []
    for i in range(0, int(sampling_rate / chunk * rec_time)):
        data = stream.read(chunk)
        frames.append(data)

    print("処理中です...")

    # 録音終了処理
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # 録音データをファイルに保存
    wav = wave.open(file_path, 'wb')
    wav.setnchannels(ch)
    wav.setsampwidth(audio.get_sample_size(fmt))
    wav.setframerate(sampling_rate)
    wav.writeframes(b''.join(frames))
    wav.close()

def voiceTOtext():
    voice_recoad()
    with skn.sr.AudioFile("output.wav") as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='ja-JP')
    return(text)


def talk(content):
    sapi = win32com.client.Dispatch("SAPI.SpVoice")
    dog = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
    dog.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
    v = [t for t in dog.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Sayaka"]
    if v:
        oldv = sapi.Voice
        sapi.Voice = v[0]
        sapi.Speak(content)
        sapi.Voice = oldv

def gameList(text):
    global gamelist, PC, Switch, PS
    l = 0
    if 'PC' in text or 'パソコン' in text or 'ゲーミング' in text:
        gamelist.extend(PC)
        l += 1
    if 'ニンテンドースイッチ' in text or 'スイッチ' in text or 'スイッチライト' in text or  'switch' in text or 'SWITCH' in text:
        gamelist.extend(Switch)
        l += 1
    if 'PleyStation' in text or 'PS' in text or 'プレイステーション' in text or 'プレステ' in text:
        gamelist.extend(PS)
        l += 1

def gamefriendORsolo(text):
    global soloflag,genreflag, reguflag, PSolopattern, Npattern, random
    if bool(PSolopattern.search(text)):
        if bool(Npattern.search(text)):
            soloflag = False
            if glflag == True:
                l = []
                for i in range(len(gamelist)):
                    if bool(gamelist[i]["solo"].search(True)):
                        l.extend(gamelist[i])
                    a = random.choice(l)
                    genreflag = a["title"]
                    reguflag = a["regu"]
        else:
            soloflag = True
    else:
        soloflag = False

def samplegametitle(text):
    global genreflag, reguflag, glflag, samplename
    for i in range(len(gamelist)):
        if bool(gamelist[i]["title"].search(text)):
            genreflag = gamelist[i]["genre"]
            reguflag = gamelist[i]["regu"]
            samplename = gamelist[i]["tname"]
            glflag =- True   

#ジャンルごとのソフト一覧
Switch=[{"addtext": "五つの大陸といくつかの島々からなる世界「アストルティア」が、、 『ドラゴンクエストテン、、オフライン』の冒険の舞台。、、、、主人公は、、五つの種族が暮らす各大陸をめぐりながら、、 仲間たちとともに魔に侵され始めたアストルティアを救う壮大な冒険に旅立ちます。、、、、				","Ntext": "RPGの代表にふれたことはありますか？","tname": "ドラゴンクエストテン　目覚めしいつつの種族オフライン","title":RPG,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
        {"addtext": "アクションとRPGが融合した「ポケモン」シリーズの最新作です。、、、、ヒスイ地方を舞台にオープンワールドの「ポケモン」を楽しみましょう。、、、、				","Ntext": "新しいポケモンを体験してみませんか？","tname": "ポケモンレジェンズアルセウス","title":RPG2,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.pokemon.co.jp/ex/legends_arceus/ja/"},
        {"addtext": "ドラクエシリーズ最新作のドラゴンクエストイレブンを紹介します。、、、、個性的で魅力のある仲間たちと、、世界を救う旅に出かけましょう。、、、、先の読めない二転三転するストーリーは、、あなたが初めてRPGをプレイした時のワクワクを思い出させてくれるかもしれません。、、、、こん作では勇者の立ち位置が過去のドラクエシリーズと違っているので、、これまでに他のドラクエをプレイしたかたも新鮮な気持ちで楽しめるでしょう。、、、、				","Ntext": "ドラゴンクエストの世界に触れてみませんか？","tname": "ドラゴンクエストイレブン　過ぎ去りしときを求めて","title":RPG3,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
        {"addtext": "2010年に発売したRPGゼノブレイドのリマスター版です。、、、、謎の生命体「機神兵」に故郷を襲われ、、幼馴染の命を奪われた主人公シュルクは、、その敵を討つため、、人類と機械が対立し合う壮大な世界の冒険へと旅立ちます。、、、、美しく壮大な冒険をお楽しみください。、、、、				","Ntext": "圧倒的なボリューム、、プレイして世界かんに浸かる貴方が見えました","tname": "ゼノブレイド","title":RPG4,"genre":"RPG","regu":"C","solo":True,"URL":"https://www.nintendo.co.jp/switch/aubqa/index.html"},
        {"addtext": "「きめつの刃」で描かれたストーリーを追体験できます。、、、、あなたも鬼を滅する刃となれ。、、、、				","Ntext": "お一人でプレイをするのが好きそうなあなたには、、アクションをおすすめします。、、、、","tname": "きめつのやいば　ヒノカミけっぷうたん","title":ACT,"genre":"アクション","regu":"C","solo":False,"URL":"https://game.kimetsu.com/hinokami/"},
        {"addtext": "「星のカービィ」最新作。、、、、星のカービィディスカバリーはシリーズ初の3Dアクションゲーム。、、、、Joy-Conをおすそわければ2人プレイに早変わり。、、、、				","Ntext": "ほおばりヘンケイによりさまざまなアクションが可能になったカービィはいかがですか？","tname": "星のカービィ　ディスカバリー","title":ACT2,"genre":"アクション","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/arzga/index.html"},
        {"addtext": "モンスターハンターライズ・サンブレイク。、、、、フィールドを自在に駆け、、強大なモンスターをハントするアクションゲーム。、、、、空中を縦横無尽に飛び回ることのできるかけりむしアクションは、、こんさくの目玉ともいえる新要素だ。、、、、				","Ntext": "1人でも、、みんなでも楽しめる、、アクションゲームはどうですか？","tname": "モンスターハンターライズ　サンブレイク","title":ACT3,"genre":"アクション","regu":"C","solo":True,"URL":"https://www.monsterhunter.com/rise-sunbreak/ja/"},
        {"addtext": "ドラゴンボールZ KAKAROTは自らが「孫悟空」となり、、圧倒的なボリュームと新しいビジュアルで描かれる「ドラゴンボールｚ」を１から辿るアクションRPG。、、、、超人的なバトル、、ぶくう術による空中散策といった超ごく体験が可能です。、、、、				","Ntext": "ドラゴンボール好きにはたまらない","tname": "ドラゴンボールゼットカカロット","title":ACTRPG,"genre":"アクションRPG","regu":"B","solo":True,"URL":"https://dbar.bn-ent.net/"},
        {"addtext": "ペルソナ5 スクランブル ザ ファントム ストライカーズは、、日本各地で発生する謎のかい事件。、、、、その背後には新たに誕生した認知世界『ジェイル』が関係していた。、、、、心の怪盗団は歪んだ大人から人々を救うため、、キャンピングカーで世直しの旅へと出発する。、、、、				","Ntext": "君も悪を滅する心の怪盗団のメンバーに","tname": "ペルソナファイブ　スクランブルザファントムストライカーズ","title":ACTRPG2,"genre":"アクションRPG","regu":"B","solo":True,"URL":"https://p5s.jp/"},
        {"addtext": "手書きのような綺麗なグラフィックに綿密に練られたシナリオと壮大かつ回収が鮮やかな伏線があるストーリーは国内外で多くの賞を受賞しています。、、、、過去、、未来の時を超えて描かれる１３人の少年少女の群像劇　序盤丸ごとの体験版もあるので試してみてください。、、、、				","Ntext": "このゲームでしか味わえない読後感を体験してみませんか？","tname": "じゅうさんきへいぼうえいけん","title":AD,"genre":"アドベンチャー","regu":"C","solo":True,"URL":"https://13sar.jp/"},
        {"addtext": "紙のようにペラペラなマリオが大冒険　本作は、、アクションとパズルが合わさった「360°パズル」システムを採用。、、、、シンプルながらも奥深いバトルをお楽しみください。、、、、				","Ntext": "ペラペラな世界で謎解きと360°バトルのアドベンチャーを体験してみませんか？","tname": "ペーパーマリオオリガミキング","title":AD2,"genre":"アドベンチャー","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/switch/aruua/index.html"},
        {"addtext": "「どうぶつの森」シリーズ最新作　無人島を舞台に釣りや虫とり、、ガーデニングやDIYなど好きなことを好きなだけ楽しめます。、、、、どうぞのんびり、、ゆったり無人とう暮らしをお楽しみください。、、、、				","Ntext": "ほのぼのとした島生活をしませんか？","tname": "あつまれどうぶつの森","title":SHUM,"genre":"シミュレーション","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/switch/acbaa/index.html"},
        {"addtext": "Stardew Valleyは、、オープンエンド式のカントリーライフシミュレーションです。、、、、自給自足の生活で草木の生い茂る土地を昔の活気があった谷に戻しましょう。、、、、				","Ntext": "自給自足のシュミレーションゲームはいかがですか？","tname": "スタードゥバレー","title":SHUM2,"genre":"シミュレーション","regu":"A","solo":True,"URL":"https://store-jp.nintendo.com/list/software/70010000005423.html"},
        {"addtext": "戦争をテーマに壮大なストーリーが展開されるシミュレーションRPG「ファイヤーエンブレム」の最新作、、舞台は3つの大国が存在する大地『フォドラ』プレーヤーは士官学校の教師となって物語を進めていきましょう。、、、、				","Ntext": "ふうかせつげつ、、この言葉がかっこいいと思った貴方はハマります","tname": "ファイアーエムブレムふうかせつげつ","title":SHUM3,"genre":"シミュレーション","regu":"B","solo":True,"URL":"https://www.nintendo.co.jp/switch/anvya/pc/index.html"},
        {"addtext": "「スプラトゥーン」シリーズの3さくめ、、舞台は「バンカラ地方」、、基本ルールはそのままにパワーアップしたバトルが楽しめます。、、、、他にも、、ミニゲームやストーリーモード、、協力プレイのサーモンランなどさまざまなモードがあり、、有限の時間の中で無限の楽しさがあります。、、、、				","Ntext": "何もかもぶちまけたい時ってありますよね、、そんな貴方に。、、、、","tname": "スプラトゥーンスリー","title":SHUT,"genre":"シューティング","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/av5ja/index.html"},
        {"addtext": "エーペックスレジェンズはFPSのゲームです。、、、、あなたは20種類以上のキャラクターを選び、、三人一組の部隊を結成します。、、、、キャラクターの固有スキルを極め、、チームメイトと協力しチャンピオンを目指します。、、、、				","Ntext": "仲間とゲームをするのが好きそうなあなたには、、シューティングゲームをおすすめします。、、、、","tname": "エーペックス","title":SHUT2,"genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
        {"addtext": "あなたは100年の眠りから覚めた主人公「リンク」となって舞台である「ハイラル」の広大な土地を駆け抜けていきます。、、、、オープンワールドの世界では、、どこまでも行ける、、そんな楽しさもあります。、、、、				","Ntext": "枠にとらわれないあなただけの冒険をしませんか？","tname": "ゼルダの伝説ブレスオブザワイルド","title":OPW,"genre":"オープンワールド","regu":"B","solo":True,"URL":"https://www.nintendo.co.jp/software/feature/zelda/index.html"},
        {"addtext": "こちらのDead by Daylightは、、プレイヤーは殺人きと生存者に分かれ、、殺人きは一人で生存者全員をエンティティに捧げることを目的とし、、生存者は4人で協力して殺人きの魔の手から逃れ、、儀式から脱出するゲームです。、、、、				","Ntext": "マルチプレイアクションのサバイバルホラーゲームはいかがですか？","tname": "デッドバイデイライト","title":HOL,"genre":"ホラー","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
        {"addtext": "リトルナイトメア2は電波塔に支配された世界で、、少年「モノ」を操作するサスペンスアドベンチャーゲームです。、、、、黄色いレインコートを被った少女「シックス」と共に、、不気味なしんりんやおぞましい学校など様々な場所で謎をといたり、、トラップを回避したり、、2人で助け合って数々の障害を乗り越え電波塔を目指します。、、、、				","Ntext": "この世界かんは唯一無二です。、、、、不気味ながら引き込まれる体験をどうぞ","tname": "リトルナイトメアツー","title":HOL2,"genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
        {"addtext": "リングフィットアドベンチャーは「リングコン」と「レッグバンド」で全身を動かしながら、、世界を救う冒険をするアドベンチャーゲームです。、、、、この旅は1日30分のトレーニングで約3か月かかる長い旅路。、、、、あなたのトレーニングの成果が、、主人公のレベルアップにも繋がるゲームです。、、、、				","Ntext": "一人だからこそできる、、フィットネスをおすすめします。、、、、","tname": "リングフィットアドベンチャー","title":FIT,"genre":"フィットネス","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/ring/"},
        {"addtext": "Fit Boxing 2は画面内のインストラクターのお手本に合わせて、、リズム感覚で全身を動かすリズム＆エクササイズゲームです。、、、、全66種類のトレーニングメニューに「健康維持」「ダイエット」「体力強化」プレイヤーの要望に合わせてコースを提案します。、、、、その日の気分で時間や強度も選べます。、、、、				","Ntext": "ボクシングを通して自分自身と対戦。、、、、エクササイズのリングじょうへようこそ","tname": "フィットボクシングツー","title":FIT2,"genre":"フィットネス","regu":"A","solo":True,"URL":"https://fitboxing.net/2/"},
        {"addtext": "Nintendo Switch Sportsがあれば、、さまざまなスポーツの競技場が集合した複合施設で、、いつでも、、誰とでも、、気軽にスポーツを楽しむことができます。、、、、また、、各競技でプロリーグが開催されており、、オンライン戦を続けることでプロ認定を受けて、、さらなる強豪に挑むことができます。、、、、				","Ntext": "スポーツする道具が無い？言い訳です。、、、、道具のハッピーセットを貴方に","tname": "ニンテンドースイッチスポーツ","title":SPO,"genre":"スポーツ","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/as8sa/"},
        {"addtext": "パワプロは、、二頭身キャラによって本格的な野球が楽しめる人気のゲームです。、、、、定番の対戦だけでなく、、オリジナル選手を育成できるモードがいろいろあるのも「パワプロ」の魅力です。、、、、				","Ntext": "キャラクターカスタマイズができる、、シュミレーションゲームをおすすめします。、、、、","tname": "イーベースボールパワフルプロ野球二千二十二","title":SPO2,"genre":"スポーツ","regu":"A","solo":False,"URL":"https://www.konami.com/pawa/2022/"},
        {"addtext": "マリオたちがカートに乗ってコースを駆け巡る「マリオカート」がデラックスになって登場。、、、、シリーズ最多の42人のキャラクターが水中、、大空、、いろいろな場所を走ります。、、、、				","Ntext": "ともだちや家族と集まって遊べる、、レースゲームをおすすめします。、、、、","tname": "マリオカートエイトデラックス","title":RA,"genre":"レーシング","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/aabpa/index.html"},
        {"addtext": "よまわり三は夜の街を探索する夜道探索アクションゲームです。、、、、幼い主人公は、、自身にかけられた呪いを解くための手がかりとなる「思い出」を探して、、夜の街をさまよいます。、、、、				","Ntext": "子どものころに感じた怖さを呼び起こす。、、、、","tname": "よまわりさん" ,"title":YACT,"genre":"夜道探索アクション","regu":"C","solo":True,"URL":"https://nippon1.jp/consumer/yomawari3/enter.html"},
]#スイッチのソフト一覧
PS=[{"addtext": "五つの大陸といくつかの島々からなる世界「アストルティア」が、、 『ドラゴンクエストテンオフライン』の冒険の舞台。、、、、主人公は、、五つの種族が暮らす各大陸をめぐりながら、、 仲間たちとともに魔に侵され始めたアストルティアを救う壮大な冒険に旅立ちます。、、、、				","Ntext": "RPGの代表にふれたことはありますか？","tname": "ドラゴンクエストテン　目覚めしいつつの種族オフライン","title":RPG,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"addtext": "ドラクエシリーズ最新作のドラゴンクエストイレブンを紹介します。、、、、個性的で魅力のある仲間たちと、、世界を救う旅に出かけましょう。、、、、先の読めない二転三転するストーリーは、、あなたが初めてRPGをプレイした時のワクワクを思い出させてくれるかもしれません。、、、、こん作では勇者の立ち位置が過去のドラクエシリーズと違っているので、、これまでに他のドラクエをプレイしたかたも新鮮な気持ちで楽しめるでしょう。、、、、				","Ntext": "ドラゴンクエストの世界に触れてみませんか？","tname": "ドラゴンクエストイレブン　過ぎ去りしときを求めて","title":RPG3,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"addtext": "手書きのような綺麗なグラフィックに綿密に練られたシナリオと壮大かつ回収が鮮やかな伏線があるストーリーは国内外で多くの賞を受賞しています。、、、、過去、、未来の時を超えて描かれる１３人の少年少女の群像劇　序盤丸ごとの体験版もあるので試してみてください。、、、、				","Ntext": "このゲームでしか味わえない読後感を体験してみませんか？","tname": "じゅうさんきへいぼうえいけん","title":AD,"genre":"アドベンチャー","regu":"C","solo":True,"URL":"https://13sar.jp/"},
    {"addtext": "エーペックスレジェンズはFPSのゲームです。、、、、あなたは20種類以上のキャラクターを選び、、三人一組の部隊を結成します。、、、、キャラクターの固有スキルを極め、、チームメイトと協力しチャンピオンを目指します。、、、、				","Ntext": "仲間とゲームをするのが好きそうなあなたには、、シューティングゲームをおすすめします。、、、、","tname": "エーペックス","title":SHUT2,"genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"addtext": "こちらのDead by Daylightは、、プレイヤーは殺人鬼と生存者に分かれ、、殺人鬼は一人で生存者全員をエンティティに捧げることを目的とし、、生存者は4人で協力して殺人鬼の魔の手から逃れ、、儀式から脱出するゲームです。、、、、				","Ntext": "マルチプレイアクションのサバイバルホラーゲームはいかがですか？","tname": "デッドバイデイライト","title":HOL,"genre":"ホラー","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
    {"addtext": "リトルナイトメア2は電波塔に支配された世界で、、少年「モノ」を操作するサスペンスアドベンチャーゲームです。、、、、黄色いレインコートを被った少女「シックス」と共に、、不気味なしんりんやおぞましい学校など様々な場所で謎をといたり、、トラップを回避したり、、2人で助け合って数々の障害を乗り越え電波塔を目指します。、、、、				","Ntext": "この世界かんは唯一無二です。、、、、不気味ながら引き込まれる体験をどうぞ","tname": "リトルナイトメアツー","title":HOL2,"genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"addtext": "マーベルズ、、スパイダーマンの最新作が登場。、、、、高校生になったマイルズ・モラレスは引っ越し先での新しい生活に順応しながら、、ピーター・パーカーに導かれて、、もう一人のスパイダーマンとしての道を歩み始める。、、、、主人公の成長、、パワーをめぐる争い、、活気に満ちたオープンワールドがあなたを楽しませてくれます。、、、、				","Ntext": "映画の世界を駆け回りたい、、と思ったことがある方におすすめします。、、、、","tname": "マーベル、、スパイダーマン","title":ACT4,"genre":"アクション","regu":"C","solo":True,"URL":"https://www.playstation.com/ja-jp/games/marvels-spider-man-remastered/"},
    {"addtext": "ドラゴンボールZ KAKAROTは自らが「孫悟空」となり、、圧倒的なボリュームと新しいビジュアルで描かれる「ドラゴンボールゼット」を1から辿るアクションRPG。、、、、超人的なバトル、、舞空術による空中散策といった超悟空体験が可能です。、、、、				","Ntext": "ドラゴンボール好きにはたまらない","tname": "ドラゴンボールゼットカカロット","title":ACTRPG,"genre":"アクション","regu":"B","solo":True,"URL":"https://dbar.bn-ent.net/"},
    {"addtext": "ペルソナ5 スクランブル ザ ファントム ストライカーズは、、日本各地で発生する謎のかい事件。、、、、その背後には新たに誕生したにんち世界『ジェイル』が関係していた。、、、、心の怪盗団は歪んだ大人から人々を救うため、、キャンピングカーで世直しの旅へと出発する。、、、、				","Ntext": "君も悪を滅する心の怪盗団のメンバーに","tname": "ペルソナファイブ　スクランブルザファントムストライカーズ","title":ACTRPG2,"genre":"アクションRPG","regu":"B","solo":True,"URL":"https://p5s.jp/"},
    {"addtext": "バンディクーが本気を出した! ついにクラッシュが完全新作で復活。、、、、お馴染みのシリーズの精神を引き継ぎ、、みんなが大好きなあの有袋類が帰って来ます!スピンアタックとジャンプで宇宙規模の戦いを駆け抜けて、、広大な新世界や意外な味方、、手強いボス戦、、そして強力な新アイテム「4つのマスク」を集めてマルチバースに平和を取り戻せ!				","Ntext": "1台の本体で一緒にあそべる、、アクションゲームをおすすめします。、、、、","tname": "クラッシュ・バンディングーフォー、、とんでもマルチバース","title":ACT5,"genre":"アクション","regu":"A","solo":False,"URL":"https://www.crashbandicoot.com/ja/crash4/home"},
    {"addtext": "バーチャル・シンガー「初音ミク」主演のリズムゲームの最新作です。、、、、初音ミクの歴史を彩った178曲のリズムゲームがプレイ可能！3Dモデルのミクさんが登場するPVや、、オリジナルPVを元にした映像でリズムゲームをお楽しみいただけます。、、、、				","Ntext": "ボカロの殿堂入り。、、、、いつだって最前線。、、、、そんな彼女の集大成を一緒に","tname": "初音ミクプロジェクトディーヴァ","title":LACT,"genre":"リズムアクション","regu":"C","solo":True,"URL":"https://miku.sega.jp/FT/"},
    {"addtext": "機械が人間よりも知的な存在となってしまった近未来の世界が舞台となる『Detroit: Become Human』では、、人類とアンドロイド双方の未来があなたの手に託されることになります。、、、、あなたが下す決断の1つ1つが、、他に類を見ないほど複雑に分岐するゲームストーリーの結末を左右します。、、、、				","Ntext": "近未来の体験をあなたに","tname": "デトロイトビカムヒューマン","title":ACT6,"genre":"アクション","regu":"D","solo":True,"URL":"https://www.playstation.com/ja-jp/games/detroit-become-human/"},
    {"addtext": "ロゴにⅧを冠した「バイオハザード　ヴィレッジ」が目指すのは誰も見たことがないサバイバルホラー。、、、、事件から生還した主人公は対バイオテロ部隊 BSAAの庇護の下。、、、、妻と愛娘と平穏な日々を過ごしていた。、、、、しかし、、幸せな生活はBSAA隊長の襲撃によって破られる。、、、、奪われた娘を取り戻すため、、イーサンは再び死地へと向かう。、、、、				","Ntext": "一人でするサバイバルホラーって楽しいですよね。、、、、","tname": "バイオハザードヴィレッジ","title":HOL3,"genre":"ホラー","regu":"D","solo":True,"URL":"https://www.capcom.co.jp/biohazard/village/"},
    {"addtext": "よまわり三は夜の街を探索する夜道探索アクションゲームです。、、、、幼い主人公は、、自身にかけられた呪いを解くための手がかりとなる「思い出」を探して、、夜の街をさまよいます。、、、、				","Ntext": "子どものころに感じた怖さを呼び起こす。、、、、","tname": "よまわりさん","title":YACT,"genre":"夜道探索アクション","regu":"C","solo":True,"URL":"https://nippon1.jp/consumer/yomawari3/enter.html"},
]
#プレステのソフト一覧

PC=[{"addtext": "五つの大陸といくつかの島々からなる世界「アストルティア」が、、 『ドラゴンクエストテン、、オフライン』の冒険の舞台。、、、、主人公は、、五つの種族が暮らす各大陸をめぐりながら、、 仲間たちとともに魔に侵され始めたアストルティアを救う壮大な冒険に旅立ちます。、、、、				","Ntext": "RPGの代表にふれたことはありますか？","tname": "ドラゴンクエストテン　目覚めしいつつの種族オフライン","title":RPG,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"addtext": "ドラクエシリーズ最新作のドラゴンクエストイレブンを紹介します。、、、、個性的で魅力のある仲間たちと、、世界を救う旅に出かけましょう。、、、、先の読めない二転三転するストーリーは、、あなたが初めてRPGをプレイした時のワクワクを思い出させてくれるかもしれません。、、、、こん作では勇者の立ち位置が過去のドラクエシリーズと違っているので、、これまでに他のドラクエをプレイしたかたも新鮮な気持ちで楽しめるでしょう。、、、、				","Ntext": "ドラゴンクエストの世界に触れてみませんか？","tname": "ドラゴンクエストイレブン　過ぎ去りしときを求めて","title":RPG3,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"addtext": "モンスターハンターライズ・サンブレイク。、、、、フィールドを自在に駆け、、強大なモンスターをハントするアクションゲーム。、、、、空中を縦横無尽に飛び回ることのできるかけりむしアクションは、、こんさくの目玉ともいえる新要素だ。、、、、				","Ntext": "1人でも、、みんなでも楽しめる、、アクションゲームはどうですか？","tname": "モンスターハンターライズ　サンブレイク","title":ACT3,"genre":"アクション","regu":"C","solo":True,"URL":"https://www.monsterhunter.com/rise-sunbreak/ja/"},
    {"addtext": "エーペックスレジェンズはFPSのゲームです。、、、、あなたは20種類以上のキャラクターを選び、、三人一組の部隊を結成します。、、、、キャラクターの固有スキルを極め、、チームメイトと協力しチャンピオンを目指します。、、、、				","Ntext": "仲間とゲームをするのが好きそうなあなたには、、シューティングゲームをおすすめします。、、、、","tname": "エーペックス","title":SHUT2,"genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"addtext": "こちらのDead by Daylightは、、プレイヤーは殺人鬼と生存者に分かれ、、殺人鬼は一人で生存者全員をエンティティに捧げることを目的とし、、生存者は4人で協力して殺人鬼の魔の手から逃れ、、儀式から脱出するゲームです。、、、、				","Ntext": "マルチプレイアクションのサバイバルホラーゲームはいかがですか？","tname": "デッドバイデイライト","title":HOL,"genre":"ホラー","regu":"Z","solo":False,"URL":"https://store-jp.nintendo.com/list/software/70010000016125.html"},
    {"addtext": "リトルナイトメア2は電波塔に支配された世界をに、、少年「モノ」を操作するサスペンスアドベンチャーゲームです。、、、、黄色いレインコートを被った少女「シックス」と共に、、不気味な深林やおぞましい学校など様々な場所で謎を解いたり、、トラップを回避したり、、2人で助け合って数々の障害を乗り越え電波塔を目指します。、、、、				","Ntext": "この世界かんは唯一無二です。、、、、不気味ながら引き込まれる体験をどうぞ","tname": "リトルナイトメアツー","title":HOL2,"genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"addtext": "マーベルズ、、スパイダーマンの最新作が登場。、、、、高校生になったマイルズ・モラレスは引っ越し先での新しい生活に順応しながら、、ピーター・パーカーに導かれて、、もう一人のスパイダーマンとしての道を歩み始める。、、、、主人公の成長、、パワーをめぐる争い、、活気に満ちたオープンワールドがあなたを楽しませてくれます。、、、、				","Ntext": "「映画の世界を駆け回りたい」と思ったことがある方におすすめします。、、、、","tname": "マーベル、、スパイダーマン","title":ACT4,"genre":"アクション","regu":"C","solo":True,"URL":"https://www.playstation.com/ja-jp/games/marvels-spider-man-remastered/"},
    {"addtext": "機械が人間よりも知的な存在となってしまった近未来の世界が舞台となる『Detroit: Become Human』では、、人類とアンドロイド双方の未来があなたの手に託されることになります。、、、、あなたが下す決断の1つ1つが、、他に類を見ないほど複雑に分岐するゲームストーリーの結末を左右します。、、、、				","Ntext": "近未来の体験をあなたに","tname": "デトロイトビカムヒューマン","title":ACT6,"genre":"アクション","regu":"D","solo":True,"URL":"https://www.playstation.com/ja-jp/games/detroit-become-human/"},
]#PCゲームソフト一覧



#セリフ
Hellotext = " 、、ゲームソフトを紹介します"
ConsoleQ = "どのゲーム機を持っていますか？"
friendORsoloQ = "ゲームは一人でプレイするのが好きですか？"
RecentlyQ = "最近なんのゲームをやりましたか？"
TimeQ = "いちにちに、どのぐらいの時間ゲームをしますか？"
Notext = "認識できませんでした"
Oktext = [' OKです ',' 了解しました ',' 分かりました ',' 確認できました']

#ブラウザを動作させるための変数
linkjp = ""
link = ""
price = ""
brand = ""
order = ""

talk(Hellotext)

talk(ConsoleQ)
print("ニンテンドースイッチ、プレイステーション、ゲーミングPCからあてはまるもの全て")
count = 0
while True:
    try:
        gameList(voiceTOtext())
        print(str(skn.random.sample(Oktext,1)))
        break
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            talk(ConsoleQ+"おっしゃっていただければ、その内容を参考におすすめのゲームを探します")
            print("ニンテンドースイッチ、プレイステーション、ゲーミングPCからあてはまるもの全て")

count = 0
talk(friendORsoloQ)
while True:
    try:
        gamefriendORsolo(voiceTOtext())
        print(str(skn.random.sample(Oktext,1)))
        break
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            talk(friendORsoloQ)

count = 0
talk(RecentlyQ)
while True:
    try:
        samplegametitle(voiceTOtext())
        print(str(skn.random.sample(Oktext,1)))
        break
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            talk(RecentlyQ)

count = 0
talk(TimeQ)
while True:
    try:
        text = voiceTOtext()
        Timehour = int(re.sub(r"\D", "", text))
        timeflag = Timehour
        break
    except:
        print(Notext)
        count += 1
        if count >= 1:
            break

outputlistT = []
outputlistF = []
solopass = False

#ゲーム機、好きなジャンル、対象年齢、ソロプレイ派かマルチ派かで絞り込み
for i in range(len(gamelist)):
    test = 0
    l_namelist = [d.get('tname') for d in outputlistT]
    if samplename == gamelist[i]["tname"]:
        continue
    if gamelist[i]["tname"] in l_namelist:
        continue
    if soloflag == gamelist[i]["solo"] and genreflag == gamelist[i]["genre"]:
        a = [{"tname":gamelist[i]["tname"],
              "title":gamelist[i]["title"],
              "genre":gamelist[i]["genre"],
              "regu":gamelist[i]["regu"],
              "solo":gamelist[i]["solo"],
              "URL":gamelist[i]["URL"],
              "Ntext":gamelist[i]["Ntext"],
              "addtext":gamelist[i]["addtext"],
              "point":3,
              "match":True}]
        outputlistT.extend(a)
    elif genreflag == gamelist[i]["genre"]:
        a = [{"tname":gamelist[i]["tname"],
              "title":gamelist[i]["title"],
              "genre":gamelist[i]["genre"],
              "regu":gamelist[i]["regu"],
              "solo":gamelist[i]["solo"],
              "URL":gamelist[i]["URL"],
              "Ntext":gamelist[i]["Ntext"],
              "addtext":gamelist[i]["addtext"],
              "point":2,
              "match":True}]
        outputlistT.extend(a)
    elif soloflag == gamelist[i]["solo"]:
        a = [{"tname":gamelist[i]["tname"],
              "title":gamelist[i]["title"],
              "genre":gamelist[i]["genre"],
              "regu":gamelist[i]["regu"],
              "solo":gamelist[i]["solo"],
              "URL":gamelist[i]["URL"],
              "Ntext":gamelist[i]["Ntext"],
              "addtext":gamelist[i]["addtext"],
              "point":1,
              "match":True}]
        outputlistT.extend(a)

for item in gamelist:
    if item in outputlistT:
        pass
    else:
        b = [{"tname":item["tname"],
             "title":item["title"],
              "genre":item["genre"],
              "regu":item["regu"],
              "solo":item["solo"],
              "URL":item["URL"],
              "Ntext":item["Ntext"],
              "addtext":item["addtext"],
              "match":False}]
              
        outputlistF.extend(b)


videolist = []
vest,good,sad = [],[],[]
"""
for i in range(len(outputlistT)):
    if len(videolist) >= 2:
        break
    if outputlistT[i]["point"] == 3:
        videolist.append(outputlistT[i])
    elif outputlistT[i]["point"] == 2 and len(videolist) <= 1:
        videolist.append(outputlistT[i])
    elif len(videolist) <= 1:
        videolist.append(outputlistT[i])
"""
a,b = skn.random.sample(outputlistT,2)
videolist.append(a)
videolist.append(b)

"""
while True:
    try:
        a = skn.random.sample(vest,1)
        videolist.append(a)
        b = skn.random.sample(good,1)
        videolist.append(b)
    except:
        try:
            b = skn.random.sample(good,1)
            videolist.append(b)
        except:
            c = skn.random.sample(sad,1)
            videolist.append(c)
    if len(videolist) >= 2:
        break
"""
a = skn.random.sample(outputlistF, 1)
videolist.append(a)
message = []

s = ""
if soloflag == True:
    s = "一人で"
else:
    s = "複数にんで"
"""
l_genre = [d.get('genre') for d in videolist]


l_solo = [d.get('solo') for d in videolist]

l_ntext = [d.get('Ntext') for d in videolist]

l_tname = [d.get('tname') for d in videolist]
"""

driver_path = "C:\\driver\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
talk("これからみっつのげーむを紹介します、、、、")
#紹介の実行　デフォルトでは１０秒おきに次のゲーム画面に移動
for i in range(2):
    webbrowser.open(videolist[i]["URL"])
    skn.time.sleep(1)
    talk(videolist[i]["Ntext"])
    talk(videolist[i]["addtext"])
    skn.time.sleep(3)

for i in range(1):
    webbrowser.open(videolist[i+2][0]["URL"])
    skn.time.sleep(1)
    talk("あなたには、新しく" + videolist[2][0]["genre"] + "をおすすめします。あなたの持っているハードで" + s + "するなら" + videolist[2][0]["tname"] + "がよいでしょう")
    talk(videolist[2][0]["addtext"])
    skn.time.sleep(1)
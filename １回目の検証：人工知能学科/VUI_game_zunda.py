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
import winsound

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
RPG = re.compile(r'ドラゴンクエストX目覚めし五つの種族オフライン|ドラゴンクエスト10オフライン|ドラクエ10オフライン|ドラクエ10|ドラクエテン')
RPG2 = re.compile(r'PokémonLEGENDSアルセウス|ポケモンアルセウス|アルセウス|ポケモン')
RPG3 = re.compile(r'ドラゴンクエストXI過ぎ去りし時を求めてS|ドラゴンクエスト11|ドラクエ11|ドラゴンクエストイレブン|ドラクエイレブン')
RPG4 = re.compile(r'XenobladeDefinitiveEdition|ゼノブレイド|ゼノブレ')
RPG5 = re.compile(r'ニーア|オートマタ|ニーア オートマタ')
RPG6 = re.compile(r'ff 14|ff14|ファイナルファンタジー 14')
ACT = re.compile(r'鬼滅の刃ヒノカミ血風譚|鬼滅の刃|きめつ|キメツ')
ACT2 = re.compile(r'星のカービィ ディスカバリー|カービィ ディスカバリー|ディスカバリー|星のカービィ|カービィ')
ACT3 = re.compile(r'モンスターハンターライズ：サンブレイク|モンハンライズ サンブレイク|サンブレイク|モンハンライズ')
ACT4 = re.compile(r'MarvelsSpider-Man:MilesMorales|マーベルスパイダーマン|スパイダーマン')
ACT5 = re.compile(r'クラッシュ・バンディングー4とんでもマルチバース|クラッシュ・バンディグ|バンディグ|バンディク')
ACT6 = re.compile(r'Detroit Become Human|デトロイト ビカム ヒューマン|デトロイト')
MUS = re.compile(r'太鼓の達人|太古の')
MUS2 = re.compile(r'初音ミクProjectDIVAFutureToneDX|プロジェクトディーヴァ|初音ミク')
MUS3 = re.compile(r'晩どり|ばんどり|バンドリ')
MUS4 = re.compile(r'サイタス|サイタスアルファ')
ACTRPG = re.compile(r'ドラゴンボールZKAKAROT|ドラゴンボール')
ACTRPG2 = re.compile(r'ペルソナ5スクランブルザファントムストライカーズ|ペルソナ5スクランブル|ペルソナファイブスクランブル|ペルソナ')
AD = re.compile(r'十三機兵防衛圏|十三|防衛兼')
AD2 = re.compile(r'ペーパーマリオオリガミキング|オリガミキング|ペーパーマリオ')
AD3 = re.compile(r'龍がごとく|龍が如く')
AD4 = re.compile(r'ラスオブアス|ラス オブ')
SHUM = re.compile(r'あつまれどうぶつの森|あつ森|動物の森|どうぶつの森')
SHUM2 = re.compile(r'StardewValley|スターデューバレー|スタードゥバレー|スターデュ|スタードゥ')
SHUM3 = re.compile(r'ファイアーエムブレム 風花雪月|風花雪月|ファイアーエムブレム')
SHUT = re.compile(r'スプラトゥーン3|Splatoon 3|スプラ3')
SHUT2 = re.compile(r'apex|エーペックス|エイベックス|エペ|えぺ')
SHUT3 = re.compile(r'ワールド ウォー|WORLD WAR|world war')
SHUT4 = re.compile(r'地球防衛軍|防衛軍')
SHUT5 = re.compile(r'ヴァロ|ヴァロ ラント|VALORANT|')
SHUT6 = re.compile(r'ワーフレーム|War Flame|WarFlame|Warflame')
OPW = re.compile(r'ゼルダの伝説ブレスオブザワイルド|ゼルダ')
OPW2 = re.compile(r'ソニック|ソニックフロンティア')
OPW3 = re.compile(r'ウィッチャー|ウィチャ')
HOL = re.compile(r'Deadby Day light|デッドバイデイライト|dbd')
HOL2 = re.compile(r'リトルナイトメア2|リトルナイトメア')
HOL3 = re.compile(r'バイオハザード ヴィレッジ|バイオ|バイオハザード')
FIT = re.compile(r'リングフィットアドベンチャー|リングフィット|リング')
FIT2 = re.compile(r'FitBoxing2|フィットボクシング|ボクシング')
SPO = re.compile(r'Nintendo Switch Sports|ニンテンドースイッチスポーツ|スイッチスポーツ')
SPO2 = re.compile(r'eBASEBALLパワフルプロ野球2022|イーベースボール|パワプロ')
RA = re.compile(r'マリオカート8デラックス|マリカー|マリカ')
RA2 = re.compile(r'カーズ|カーズ3|カーズ 3')
RA3 = re.compile(r'カービィのグルメフェス|グルメフェス')
YACT = re.compile(r'夜廻三|夜回りさん|よまわりさん')
#喋るための準備
r = skn.sr.Recognizer()

#関数
#音声録音
def voice_recoad(T):
    rec_time = T         # 録音時間[s]
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

def voiceTOtext(T=10):
    voice_recoad(T)
    with skn.sr.AudioFile("output.wav") as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='ja-JP')
    print(text)
    return(text)

"""
def talk(content):
    sapi = win32com.client.Dispatch("SAPI.Spvoice")
    dog = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
    dog.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\voices", False)
    v = [t for t in dog.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Sayaka"]
    if v:
        oldv = sapi.voice
        sapi.voice = v[0]
        sapi.Speak(content)
        sapi.voice = oldv
"""

def gameList(text):
    global gamelist, PC, Switch, PS
    l = 0
    if 'PC' in text or 'パソコン' in text or 'ゲーミング' in text:
        gamelist.extend(PC)
        l += 1
    if 'ニンテンドースイッチ' in text or 'スイッチ' in text or 'スイッチライト' in text or  'switch' in text or 'SWITCH' in text:
        gamelist.extend(Switch)
        l += 1
    if 'PlayStation' in text or 'PS' in text or 'プレイステーション' in text or 'プレステ' in text:
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
            glflag = True


#テンプレート =         {"addtext": "", "Ntext": "", "tname":"", "title": "", "genre": "", "regu": "", "solo": "", "URL" : "",},
#ジャンルごとのソフト一覧
Switch=[{"addtext": "voice\DQ10off_addtext.wav","Ntext": "voice\DQ10off_ntext.wav","tname": "voice\DQ10off_tname.wav","title":RPG,"genre":"voice\RPG.wav","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
        {"addtext": "voice\Pokemon_addtext.wav","Ntext": "voice\Pokemon_ntext.wav","tname": "voice\Pokemon_tname.wav","title":RPG2,"genre":"voice\RPG.wav","regu":"A","solo":True,"URL":"https://www.pokemon.co.jp/ex/legends_arceus/ja/"},
        {"addtext": "voice\DQ11_addtext.wav","Ntext": "voice\DQ11_ntext.wav","tname": "voice\DQ11_tname.wav","title":RPG3,"genre":"voice\RPG.wav","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
        {"addtext": "voice\Zeno_addtext.wav","Ntext": "voice\Zeno_ntext.wav","tname": "voice\Zeno_tname.wav","title":RPG4,"genre":"voice\RPG.wav","regu":"C","solo":True,"URL":"https://www.nintendo.co.jp/switch/aubqa/index.html"},
        {"addtext": "voice\kimetu_addtext.wav","Ntext": "voice\kimetu_ntext.wav","tname": "voice\kimetu_tname.wav","title":ACT,"genre":"voice\ACT.wav","regu":"C","solo":False,"URL":"https://game.kimetsu.com/hinokami/"},
        {"addtext": "voice\kirby_addtext.wav","Ntext": "voice\kirby_ntext.wav","tname": "voice\kirby_tname.wav","title":ACT2,"genre":"voice\ACT.wav","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/arzga/index.html"},
        {"addtext": "voice\MHR_addtext.wav","Ntext": "voice\MHR_ntext.wav","tname": "voice\MHR_tname.wav","title":ACT3,"genre":"voice\ACT.wav","regu":"C","solo":True,"URL":"https://www.monsterhunter.com/rise-sunbreak/ja/"},
        {"addtext": "voice\DB_addtext.wav","Ntext": "voice\DB_ntext.wav","tname": "voice\DB_tname.wav","title":ACTRPG,"genre":"voice\ACT.wav","regu":"B","solo":True,"URL":"https://dbar.bn-ent.net/"},
        {"addtext": "voice\P5_addtext.wav","Ntext": "voice\P5_ntext.wav","tname": "voice\P5_tname.wav","title":ACTRPG2,"genre":"voice\ACT.wav","regu":"B","solo":True,"URL":"https://p5s.jp/"},
        {"addtext": "voice\Jusan_addtext.wav","Ntext": "voice\Jusan_ntext.wav","tname": "voice\Jusan_tname.wav","title":AD,"genre":"voice\ADV.wav","regu":"C","solo":True,"URL":"https://13sar.jp/"},
        {"addtext": "voice\mario_addtext.wav","Ntext": "voice\mario_addtext.wav","tname": "voice\mario_tname.wav","title":AD2,"genre":"voice\ADV.wav","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/switch/aruua/index.html"},
        {"addtext": "voice\dmori_addtext.wav","Ntext": "voice\dmori_ntext.wav","tname": "voice\dmori_tname.wav","title":SHUM,"genre":"voice\SMU.wav","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/switch/acbaa/index.html"},
        {"addtext": "voice\Stardo_addtext.wav","Ntext": "voice\Stardo_ntext.wav","tname": "voice\Stardo_tname.wav","title":SHUM2,"genre":"voice\SMU.wav","regu":"A","solo":True,"URL":"https://store-jp.nintendo.com/list/software/70010000005423.html"},
        {"addtext": "voice\FE_addtext.wav","Ntext": "voice\FE_ntext.wav","tname": "voice\FE_tname.wav","title":SHUM3,"genre":"voice\SMU.wav","regu":"B","solo":True,"URL":"https://www.nintendo.co.jp/switch/anvya/pc/index.html"},
        {"addtext": "voice\spla_addtext.wav","Ntext": "voice\spla_ntext.wav","tname": "voice\spla_tname.wav","title":SHUT,"genre":"voice\SHUT.wav","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/av5ja/index.html"},
        {"addtext": "voice\Apex_addtext.wav","Ntext": "voice\Apex_ntext.wav","tname": "voice\Apex_tname.wav","title":SHUT2,"genre":"voice\SHUT.wav","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
        {"addtext": "voice\link_addtext.wav","Ntext": "voice\link_ntext.wav","tname": "voice\link_tname.wav","title":OPW,"genre":"voice\OPEN.wav","regu":"B","solo":True,"URL":"https://www.nintendo.co.jp/software/feature/zelda/index.html"},
        {"addtext": "voice\DBD_addtext.wav","Ntext": "voice\DBD_ntext.wav","tname": "voice\DBD_tname.wav","title":HOL,"genre":"voice\HOL.wav","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
        {"addtext": "voice\Lnight_addtext.wav","Ntext": "voice\Lnight_ntext.wav","tname": "voice\Lnight_tname.wav","title":HOL2,"genre":"voice\HOL.wav","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
        {"addtext": "voice\ling_addtext.wav","Ntext": "voice\ling_ntext.wav","tname": "voice\ling_tname.wav","title":FIT,"genre":"voice\ADV.wav","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/ring/"},
        {"addtext": "voice\FitB_addtext.wav","Ntext": "voice\FitB_ntext.wav","tname": "voice\FitB_tname.wav","title":FIT2,"genre":"voice\SPO.wav","regu":"A","solo":True,"URL":"https://fitboxing.net/2/"},
        {"addtext": "voice\msport_addtext.wav","Ntext": "voice\msport_ntext.wav","tname": "voice\msport_tname.wav","title":SPO,"genre":"voice\SPO.wav","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/as8sa/"},
        {"addtext": "voice\pawapro_addtext.wav","Ntext": "voice\pawapro_ntext.wav","tname": "voice\pawapro_tname.wav","title":SPO2,"genre":"voice\SPO.wav","regu":"A","solo":False,"URL":"https://www.konami.com/pawa/2022/"},
        {"addtext": "voice\Mcar_addtext.wav","Ntext": "voice\Mcar_ntext.wav","tname": "voice\Mcar_tname.wav","title":RA,"genre":"voice\RACE.wav","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/aabpa/index.html"},
        {"addtext": "voice\yomawari_addtext.wav","Ntext": "voice\yomawari_ntext.wav","tname": "voice\yomawari_tname.wav" ,"title":YACT,"genre":"voice\HOL.wav","regu":"C","solo":True,"URL":"https://nippon1.jp/consumer/yomawari3/enter.html"},
        {"addtext": "voice\WWZ_addtext.wav", "Ntext": "voice\WWZ_addtext.wav", "tname":"voice\WWZ_tname.wav", "title": SHUT3, "genre": "voice\SHUT.wav", "regu": "Z", "solo": False, "URL" : "http://www.h2int.com/games/wwz/#target",},
        {"addtext": "voice\TT_addtext.wav", "Ntext": "voice\TT_ntext.wav", "tname":"voice\TT_ntext.wav", "title": MUS, "genre": "voice\MUS.wav", "regu": "A", "solo": False, "URL" : "https://switch.taiko-ch.net/",},
        {"addtext": "voice\BD_addtext.wav", "Ntext": "voice\BD_ntext.wav", "tname":"voice\BD_tname.wav", "title": MUS3, "genre": "voice\MUS.wav", "regu": "B", "solo": True, "URL" : "https://bang-dream.bushimo.jp/switch/",},
        {"addtext": "voice\Carz_addtext.wav", "Ntext": "voice\Carz_ntext.wav", "tname":"voice\Carz_tname.wav", "title": RA2, "genre": "voice\RACE.wav", "regu": "A", "solo" :False, "URL" : "https://warnerbros.co.jp/game/cars3/"},
        {"addtext": "voice\Sonic_addtext.wav", "Ntext": "voice\Sonic_ntext.wav", "tname":"Sonic_tname.wav", "title": OPW2, "genre": "voice\OPEN.wav", "regu": "A", "solo": True, "URL" : "https://sonic.sega.jp/SonicFrontiers/",},
        {"addtext": "voice\Wit3_addtext.wav", "Ntext": "voice\Wit3_ntext.wav", "tname":"Wit3_tname.wav", "title": OPW3, "genre": "voice\OPEN.wav", "regu": "Z", "solo": True, "URL" : "https://www.spike-chunsoft.co.jp/witcher3/ns/",},
        {"addtext": "voice\KBfes_addtext.wav", "Ntext": "voice\KBfes_ntext.wav", "tname":"voice\KBfes_ntext.wav", "title": RA3, "genre": "voice\RACE.wav", "regu": "A", "solo": False, "URL" : "https://www.nintendo.co.jp/switch/a59xa/index.html",},
        {"addtext": "voice\Syt_addtext.wav", "Ntext": "voice\Syt_ntext.wav", "tname":"voice\Syt_tname", "title": MUS4, "genre": "voice\MUS.wav", "regu": "A", "solo": False, "URL" : "https://cytusalpha.com/",},
        ]#スイッチのソフト一覧

PS=[{"addtext": "voice\DQ10off_addtext.wav","Ntext": "voice\DQ10off_ntext.wav","tname": "voice\DQ10off_tname.wav","title":RPG,"genre":"voice\RPG.wav","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"addtext": "voice\DQ11_addtext.wav","Ntext": "voice\DQ11_ntext.wav","tname": "voice\DQ11_tname.wav","title":RPG3,"genre":"voice\RPG.wav","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"addtext": "voice\Jusan_addtext.wav","Ntext": "voice\Jusan_ntext.wav","tname": "voice\Jusan_tname.wav","title":AD,"genre":"voice\ADV.wav","regu":"C","solo":True,"URL":"https://13sar.jp/"},
    {"addtext": "voice\Apex_addtext.wav","Ntext": "voice\Apex_ntext.wav","tname": "voice\Apex_tname.wav","title":SHUT2,"genre":"voice\SHUT.wav","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"addtext": "voice\DBD_addtext.wav","Ntext": "voice\DBD_ntext.wav","tname": "voice\DBD_tname.wav","title":HOL,"genre":"voice\HOL.wav","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
    {"addtext": "voice\Lnight_addtext.wav","Ntext": "voice\Lnight_ntext.wav","tname": "voice\Lnight_tname.wav","title":HOL2,"genre":"voice\HOL.wav","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"addtext": "voice\kumo_addtext.wav","Ntext": "voice\kumo_ntext.wav","tname": "voice\kumo_tname.wav","title":ACT4,"genre":"voice\ACT.wav","regu":"C","solo":True,"URL":"https://www.playstation.com/ja-jp/games/marvels-spider-man-remastered/"},
    {"addtext": "voice\DB_addtext.wav","Ntext": "voice\DB_ntext.wav","tname": "voice\DB_tname.wav","title":ACTRPG,"genre":"voice\ACT.wav","regu":"B","solo":True,"URL":"https://dbar.bn-ent.net/"},
    {"addtext": "voice\P5_addtext.wav","Ntext": "voice\P5_ntext.wav","tname": "voice\P5_tname.wav","title":ACTRPG2,"genre":"voice\ACT.wav","regu":"B","solo":True,"URL":"https://p5s.jp/"},
    {"addtext": "voice\Bandy_addtext.wav","Ntext": "voice\Bandy_ntext.wav","tname": "voice\Bandy_tname.wav","title":ACT5,"genre":"voice\ACT.wav","regu":"A","solo":False,"URL":"https://www.crashbandicoot.com/ja/crash4/home"},
    {"addtext": "voice\DBH_addtext.wav","Ntext": "voice\DBH_ntext.wav","tname": "voice\DBH_tname.wav","title":ACT6,"genre":"voice\ACT.wav","regu":"D","solo":True,"URL":"https://www.playstation.com/ja-jp/games/detroit-become-human/"},
    {"addtext": "voice\Vaio_addtext.wav","Ntext": "voice\Vaio_ntext.wav","tname": "voice\Vaio_tname.wav","title":HOL3,"genre":"voice\HOL.wav","regu":"D","solo":True,"URL":"https://www.capcom.co.jp/biohazard/village/"},
    {"addtext": "voice\yomawari_addtext.wav","Ntext": "voice\yomawari_ntext.wav","tname": "voice\yomawari_tname.wav" ,"title":YACT,"genre":"voice\HOL.wav","regu":"C","solo":True,"URL":"https://nippon1.jp/consumer/yomawari3/enter.html"},
    {"addtext": "voice\TB_addtext.wav", "Ntext": "voice\TB_ntext.wav", "tname":"voice\TB_tname.wav", "title": SHUT4, "genre": "voice\SHUT.wav", "regu": "D", "solo": False, "URL" : "https://www.d3p.co.jp/edf5/"},
    {"addtext": "voice\WWZ_addtext.wav", "Ntext": "voice\WWZ_addtext.wav", "tname":"voice\WWZ_tname.wav", "title": SHUT3, "genre": "voice\SHUT.wav", "regu": "Z", "solo": False, "URL" : "http://www.h2int.com/games/wwz/#target",},
    {"addtext": "voice\Meir_addtext.wav", "Ntext": "voice\Meir_ntext.wav", "tname":"voice\Meir_tname.wav", "title": RPG5, "genre": "voice\RPG.wav", "regu": "D", "solo": True, "URL" : "https://www.jp.square-enix.com/nierautomata/"},
    {"addtext": "voice\Ryuga_addtext.wav", "Ntext": "voice\Ryuga_ntext.wav", "tname":"voice\Ryuga_tname.wav", "title": AD3, "genre": "voice\ADV.wav", "regu": "D", "solo": True, "URL" : "https://ryu-ga-gotoku.com/kiwami/"},
    {"addtext": "voice\Lous_addtext.wav", "Ntext": "voice\Lous_ntext.wav", "tname":"voice\Lous_tname.wav", "title": AD4, "genre": "voice\ADV.wav", "regu": "Z", "solo": True, "URL" : "https://www.playstation.com/ja-jp/games/the-last-o"},
]
#{"addtext": "voice\miku_addtext.wav","Ntext": "voice\miku_ntext.wav","tname": "voice\miku_tname.wav","title":MUS2,"genre":"音ゲー","regu":"C","solo":True,"URL":"https://miku.sega.jp/FT/"},
#プレステのソフト一覧

PC=[{"addtext": "voice\DQ10off_addtext.wav","Ntext": "voice\DQ10off_ntext.wav","tname": "voice\DQ10off_tname.wav","title":RPG,"genre":"voice\RPG.wav","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"addtext": "voice\DQ11_addtext.wav","Ntext": "voice\DQ11_ntext.wav","tname": "voice\DQ11_tname.wav","title":RPG3,"genre":"voice\RPG.wav","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"addtext": "voice\MHR_addtext.wav","Ntext": "voice\MHR_ntext.wav","tname": "voice\MHR_tname.wav","title":ACT3,"genre":"voice\ACT.wav","regu":"C","solo":True,"URL":"https://www.monsterhunter.com/rise-sunbreak/ja/"},
    {"addtext": "voice\Apex_addtext.wav","Ntext": "voice\Apex_ntext.wav","tname": "voice\Apex_tname.wav","title":SHUT2,"genre":"voice\SHUT.wav","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"addtext": "voice\DBD_addtext.wav","Ntext": "voice\DBD_ntext.wav","tname": "voice\DBD_tname.wav","title":HOL,"genre":"voice\HOL.wav","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
    {"addtext": "voice\Lnight_addtext.wav","Ntext": "voice\Lnight_ntext.wav","tname": "voice\Lnight_tname.wav","title":HOL2,"genre":"voice\HOL.wav","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"addtext": "voice\kumo_addtext.wav","Ntext": "voice\kumo_ntext.wav","tname": "voice\kumo_tname.wav","title":ACT4,"genre":"voice\ACT.wav","regu":"C","solo":True,"URL":"https://www.playstation.com/ja-jp/games/marvels-spider-man-remastered/"},
    {"addtext": "voice\DBH_addtext.wav","Ntext": "voice\DBH_ntext.wav","tname": "voice\DBH_tname.wav","title":ACT6,"genre":"voice\ACT.wav","regu":"D","solo":True,"URL":"https://www.playstation.com/ja-jp/games/detroit-become-human/"},
    {"addtext": "voice\Valo_addtext.wav", "Ntext": "voice\Valo_addtext.wav", "tname":"voice\Valo_addtext.wav", "title": SHUT5, "genre": "voice\SHUT.wav", "regu": "B", "solo": False, "URL" : "https://playvalorant.com/ja-jp/",},
    {"addtext": "voice\FF14_addtext.wav", "Ntext": "voice\FF14_ntext.wav", "tname":"voice\FF14_tname.wav", "title": RPG6, "genre": "voice\RPG.wav", "regu": "C", "solo": False, "URL" : "https://jp.finalfantasyxiv.com/",},
    {"addtext": "voice\Vaio_addtext.wav","Ntext": "voice\Vaio_ntext.wav","tname": "voice\Vaio_tname.wav","title":HOL3,"genre":"voice\HOL.wav","regu":"D","solo":True,"URL":"https://www.capcom.co.jp/biohazard/village/"},
    {"addtext": "voice\WF_addtext.wav", "Ntext": "voice\WF_ntext.wav", "tname":"voice\WF_tname.wav", "title": SHUT6, "genre": "voice\SHUT.wav", "regu": "Z", "solo": False, "URL" : "https://store.steampowered.com/app/230410/Warframe/?l=japanese",},
]#PCゲームソフト一覧

#セリフ
Hellotext = "voice\Hellotext.wav"
ConsoleQ = "voice\ConsoleQ.wav"
friendORsoloQ = "voice\FriendORsoloQ.wav"
RecentlyQ = "voice\RecentlyQ.wav"
TimeQ = "voice\TimeQ.wav"
Notext = "認識できませんでした"
Oktext = [' OKです ',' 了解しました ',' 分かりました ',' 確認できました']

#ブラウザを動作させるための変数
linkjp = ""
link = ""
price = ""
brand = ""
order = ""

winsound.PlaySound(Hellotext, winsound.SND_FILENAME)

winsound.PlaySound(ConsoleQ, winsound.SND_FILENAME)
print("ニンテンドースイッチ、プレイステーション、ゲーミングPCからあてはまるもの全て")
count = 0
while True:
    try:
        gameList(voiceTOtext())
        #gameList("ニンテンドースイッチ")
        print(str(skn.random.sample(Oktext,1)))
        break
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            winsound.PlaySound(ConsoleQ, winsound.SND_FILENAME)
            print("ニンテンドースイッチ、プレイステーション、ゲーミングPCからあてはまるもの全て")


count = 0
winsound.PlaySound(friendORsoloQ, winsound.SND_FILENAME)
while True:
    try:
        gamefriendORsolo(voiceTOtext(5))
        #gamefriendORsolo("ソロ")
        print(str(skn.random.sample(Oktext,1)))
        break
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            winsound.PlaySound(friendORsoloQ, winsound.SND_FILENAME)

count = 0
winsound.PlaySound(RecentlyQ, winsound.SND_FILENAME)
while True:
    try:
        samplegametitle(voiceTOtext())
        #samplegametitle("オクトパストラベラー")
        print(str(skn.random.sample(Oktext,1)))
        break
    except:
        print("認識できませんでした")
print(genreflag)
if genreflag == "":
    winsound.PlaySound("voice\GenreQ.wav", winsound.SND_FILENAME)
    l = []
    memo = []
    while True:
        try:
            for i in range(len(gamelist)):
                if gamelist[i]["genre"] in memo:
                    pass
                else:
                    t = ""
                    if gamelist[i]["genre"] == "voice\RPG.wav":
                        t = "RPG"
                    if gamelist[i]["genre"] == "voice\ACT.wav":
                        t = "アクション"
                    if gamelist[i]["genre"] == "voice\ADV.wav":
                        t = "アドベンチャー"
                    if gamelist[i]["genre"] == "voice\HOL.wav":
                        t = "ホラー"
                    if gamelist[i]["genre"] == "voice\MUS.wav":
                        t = "音ゲー"
                    if gamelist[i]["genre"] == "voice\OPEN.wav":
                        t = "オープンワールド"
                    if gamelist[i]["genre"] == "voice\RACE.wav":
                        t = "レーシング"
                    if gamelist[i]["genre"] == "voice\SHUT.wav":
                        t = "シューティング"
                    if gamelist[i]["genre"] == "voice\SMU.wav":
                        t = "シミュレーション"
                    if gamelist[i]["genre"] == "voice\SPO.wav":
                        t = "スポーツ"
                    l.append(t)
                memo.append(gamelist[i]["genre"])
            print("次のジャンルからひとつだけ")
            print(l)
            text = voiceTOtext(5)
            #text = "RPG"
            #print(text)
            if text in l:
                t = ""
                if text == "RPG":
                    t = "voice\RPG.wav"
                if text == "アクション":
                    t = "voice\ACT.wav"
                if text == "アドベンチャー":
                    t = "voice\ADV.wav"
                if text == "ホラー":
                    t = "voice\HOL.wav"
                if text == "音ゲー":
                    t = "voice\MUS.wav"
                if text == "オープンワールド":
                    t = "voice\OPEN.wav"
                if text == "レーシング":
                    t = "voice\RACE.wav"
                if text == "シューティング":
                    t = "voice\SHUT.wav"
                if text == "シミュレーション":
                    t = "voice\SMU.wav"
                if text == "スポーツ":
                    t = "voice\SPO.wav"
                genreflag = t
                break
        except:
            print("認識できませんでした")
#print(genreflag)
count = 0
winsound.PlaySound(TimeQ, winsound.SND_FILENAME)
while True:
    try:
        text = voiceTOtext(5)
        #text = "2時間"
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
videolist = []
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
        a = [{"addtext":gamelist[i]["addtext"],
              "Ntext":gamelist[i]["Ntext"],
              "tname":gamelist[i]["tname"],
              "title":gamelist[i]["title"],
              "genre":gamelist[i]["genre"],
              "regu":gamelist[i]["regu"],
              "solo":gamelist[i]["solo"],
              "URL":gamelist[i]["URL"]},
              ]
        videolist.extend(a)
    elif genreflag == gamelist[i]["genre"]:
        a = [{"addtext":gamelist[i]["addtext"],
              "Ntext":gamelist[i]["Ntext"],
              "tname":gamelist[i]["tname"],
              "title":gamelist[i]["title"],
              "genre":gamelist[i]["genre"],
              "regu":gamelist[i]["regu"],
              "solo":gamelist[i]["solo"],
              "URL":gamelist[i]["URL"]},
              ]
        videolist.extend(a)
    if len(videolist) >= 2:
        break

for item in gamelist:
    if item in outputlistT:
        pass
    else:
        b = [{"addtext":item["addtext"],
              "Ntext":item["Ntext"],
              "tname":item["tname"],
              "title":item["title"],
              "genre":item["genre"],
              "regu":item["regu"],
              "solo":item["solo"],
              "URL":item["URL"],}
              ]
              
        outputlistF.extend(b)

#vest,good,sad = [],[],[]
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

for i in range(len(outputlistT)):
    if outputlistT[i]["solo"] == soloflag:
        videolist.append(outputlistT[i])
        if len(outputlistT) >= 2:
            break
    else:
        videolist.append(outputlistT[i])


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

outputF = []#outputlistFからプレイ人数でフィルタリング
for i in range(len(outputlistF)):
    if outputlistF[i]["solo"] == soloflag:
        b = [{"addtext":outputlistF[i]["addtext"],
              "Ntext":outputlistF[i]["Ntext"],
              "tname":outputlistF[i]["tname"],
              "title":outputlistF[i]["title"],
              "genre":outputlistF[i]["genre"],
              "regu":outputlistF[i]["regu"],
              "solo":outputlistF[i]["solo"],
              "URL":outputlistF[i]["URL"],}
              ]
        outputF.extend(b)
"""
for i in range(2):
    videolist.extend(outputlistT[i])
"""

a = skn.random.sample(outputF, 1)
videolist.extend(a)
message = []

s = ""
if soloflag == True:
    s = "voice\Solo1.wav"
else:
    s = "voice\solo2.wav"
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
winsound.PlaySound("voice\start.wav", winsound.SND_FILENAME)
#紹介の実行　デフォルトでは１０秒おきに次のゲーム画面に移動
#print(videolist)
for i in range(2):
    webbrowser.open(videolist[i]["URL"])
    skn.time.sleep(1)
    winsound.PlaySound(videolist[i]["Ntext"], winsound.SND_FILENAME)
    winsound.PlaySound(videolist[i]["addtext"], winsound.SND_FILENAME)
    skn.time.sleep(3)

for i in range(1):
    webbrowser.open(videolist[i+2]["URL"])
    skn.time.sleep(1)
    winsound.PlaySound("voice\Ftalk1.wav", winsound.SND_FILENAME)
    winsound.PlaySound(videolist[2]["genre"], winsound.SND_FILENAME)
    winsound.PlaySound("voice\Ftalk2.wav", winsound.SND_FILENAME)
    winsound.PlaySound(s, winsound.SND_FILENAME)
    winsound.PlaySound("voice\Ftalk3-5.wav", winsound.SND_FILENAME)
    winsound.PlaySound(videolist[2]["tname"], winsound.SND_FILENAME)
    winsound.PlaySound("voice\Ftalk4.wav", winsound.SND_FILENAME)
    winsound.PlaySound(videolist[2]["addtext"], winsound.SND_FILENAME)
    skn.time.sleep(1)

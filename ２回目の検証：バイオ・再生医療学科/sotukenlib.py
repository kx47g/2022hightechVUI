# -*- coding: utf-8 -*-
from tkinter.constants import E
import keyboard
import sys
import tkinter
from PIL import Image, ImageTk
import threading
import time
import winsound
import simpleaudio
import wave
import pyaudio
#音声処理用ライブラリ
import speech_recognition as sr
#発話用ライブラリ
import win32com.client
# Webサイトにアクセスするためのライブラリ
import requests
# Webページの中のデータにアクセスできるようにするためのライブラリ
from bs4 import BeautifulSoup
#Web検索を行えるライブラリ
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import urllib
#文字列から抽出
import re
import random

talk_sleep = re.compile(r'静かに|黙って|黙れ|うるさい|やかましい|いつまで|めんど|邪魔|もういい|もうええ|うっとおしい|鬱陶しい')

#喋るための準備
r = sr.Recognizer()

def show_image():
#外から触れるようにグローバル変数で定義
    global root, txt, value,canvas ,item, icon, mes, brankicon, tkinter, Image, ImageTk

    root = tkinter.Tk()
    root.title('test')
    root.geometry("250x400+1600+550")
    canvas = tkinter.Canvas(bg = "white", width=250, height=400)
    canvas.place(x=0, y=0)
    img = Image.open('defaultimage.jpg')
    img= ImageTk.PhotoImage(img)
    brankicon = Image.open('icon_brank.jpg')
    brankicon = ImageTk.PhotoImage(brankicon)
    brankmessage = Image.open('mes_brank.jpg')
    brankmessage = ImageTk.PhotoImage(brankmessage)
    item = canvas.create_image(0, 100, image=img, anchor=tkinter.NW)
    icon = canvas.create_image(0, 0, image=brankicon, anchor=tkinter.NW)
    mes = canvas.create_image(80, 10, image=brankmessage, anchor=tkinter.NW)
    root.mainloop()

#音声録音
def voice_recoad():
    global pyaudio, wave, icon, canvas
    imglisning = Image.open('icon_lisning.jpg')
    imglisning = ImageTk.PhotoImage(imglisning)
    lisningmessage = Image.open('mes_lisning.jpg')
    lisningmessage = ImageTk.PhotoImage(lisningmessage)
    canvas.itemconfig(icon,image = imglisning)
    canvas.itemconfig(mes,image = lisningmessage)
    rec_time = 5            # 録音時間[s]
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
    print("recording start...")
    # 録音処理
    frames = []
    for i in range(0, int(sampling_rate / chunk * rec_time)):
        data = stream.read(chunk)
        frames.append(data)

    print("recording  end...")

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
    global r, startflag
    voice_recoad()
    with sr.AudioFile("output.wav") as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='ja-JP')
    print(text)
    return(text)

def talk_noimg(content):
    global win32com
    sapi = win32com.client.Dispatch("SAPI.SpVoice")
    dog = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
    dog.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)

    v = [t for t in dog.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Sayaka"]
    if v:
        oldv = sapi.Voice
        sapi.Voice = v[0]
        sapi.Speak(content)
        sapi.Voice = oldv

def talk(content):
    global win32com, icon
    brankicon = Image.open('icon_brank.jpg')
    brankicon = ImageTk.PhotoImage(brankicon)
    brankmessage = Image.open('mes_brank.jpg')
    brankmessage = ImageTk.PhotoImage(brankmessage)
    canvas.itemconfig(icon,image = brankicon)
    canvas.itemconfig(mes,image = brankmessage)
    sapi = win32com.client.Dispatch("SAPI.SpVoice")
    dog = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
    dog.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)

    v = [t for t in dog.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Sayaka"]
    if v:
        oldv = sapi.Voice
        sapi.Voice = v[0]
        sapi.Speak(content)
        sapi.Voice = oldv

def sound_effect(filename):
    global simpleaudio
    wav_obj = simpleaudio.WaveObject.from_wave_file(filename)
    play_obj = wav_obj.play()
    play_obj.wait_done()

def erroroutput(text):
    f = open('errortext.txt', 'a')

    datalist = [text]
    f.writelines(datalist)

    f.close()
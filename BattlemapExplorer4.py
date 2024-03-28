from pygame.locals import *
import pygame
import sys
import settings
from concurrent.futures import ThreadPoolExecutor

import tkinter as tk
from tkinter import scrolledtext
import requests
import win32com.client
import os

def TextArea():
    speak_flg = False

    f = open('api_key.txt', 'r')
    api_key = f.read()
    f.close()

    f = open('prompt.txt', 'r', encoding="UTF-8")
    prompt = f.read()
    f.close()

    logrole = []
    logcontent = []
    logflg = os.path.isfile('log.txt')
    if logflg:
        with open('log.txt', 'r', encoding="UTF-8") as f:
            for line in f:
                linearray = line.split("<delimiter>")
                logrole.append(linearray[0])
                logcontent.append(linearray[1])

    messages = [
        {"role": "system", "content": prompt}
    ]

    log = []

    for role, i in logrole:
        messages.append({"role": role, "content": logcontent[i]})
        log.append({"role": role, "content": logcontent[i]})

    def send_request():
        # api_key.txt = os.getenv('API_KEY')  # ここでAPIキーを設定
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        messages.append({"role": "user", "content": entry.get()}) # ユーザーの入力を使用
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages
        }
        log.append({"role": "user", "content": entry.get()})

        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        print(response_data)
        response_text = response_data['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": response_text})  # ユーザーの入力を使用
        log.append({"role": "assistant", "content": response_text})
        text_area.configure(state='normal')  # テキストエリアを編集可能に
        text_area.delete('1.0', tk.END)  # 既存のテキストをクリア
        text_area.insert(tk.INSERT, response_text)  # 新しい応答を挿入
        text_area.configure(state='disabled')  # テキストエリアを再度編集不可
        entry.delete(0, tk.END)
        if speak_flg:
            speech = win32com.client.Dispatch("Sapi.SpVoice")
            speech.Speak(response_text)

        #データ保存
        #f = open('log.txt', 'w', encoding="UTF-8")
        logstr = ""
        for l in log:
            logstr = l["role"] + "<delimiter>" + l["content"] + "\n"

        logstr = logstr[:-1]
        f.write(logstr)
        f.close()

    def press_enter(self):
        # 入力内容を表示
        send_request()

        # GUIウィンドウの作成
    window = tk.Tk()
    window.title("Conversation GUI")

    # プロンプトの入力欄
    entry = tk.Entry(window, width=50)
    entry.bind("<Return>", press_enter)
    entry.pack(pady=10)

    # 応答ボタン
    send_button = tk.Button(window, text="Send", command=send_request)
    send_button.pack(pady=5)

    # 応答を表示するテキストエリア
    text_area = scrolledtext.ScrolledText(window, width=60, height=10, state='disabled')
    text_area.pack(pady=10)

    #speech = win32com.client.Dispatch("Sapi.SpVoice")

    # ウィジェット作成
    # Enterキーとボタンクリックイベントをバインド

    window.mainloop()

def main():
    pygame.init()  # Pygameを初期化
    screenx = 1440
    screeny = 900
    speed = settings.speed
    defspeed = speed
    avatarpix = settings.avatarpix
    mapzoom = settings.mapzoom
    followerx = 200
    followery = 0
    followermin = -200
    followermax = 200

    with open("zoom.txt") as f:
        print(f)
        mapzoom = float(f.read())
        # <class '_io.TextIOWrapper'>

    screen = pygame.display.set_mode((screenx, screeny))  # 画面を作成
    pygame.display.set_caption("PNGMap Explorer")  # タイトルを作成
    img2xdest = 0
    img2ydest = 0
    img3xdest = followerx
    img3ydest = followery
    # 普通に画像を表示する方法
    img1 = pygame.image.load("map/map.png")
    img1xsize = img1.get_width()
    img1ysize = img1.get_height()
    img1xsize2 = img1xsize * mapzoom
    img1ysize2 = img1ysize * mapzoom

    img1 = pygame.transform.scale(img1, (img1xsize2, img1ysize2))
    mapx, mapy = img1.get_size()
    img2xdest = (screenx // 2) - (avatarpix // 2)
    img2ydest = (screeny // 2) - (avatarpix // 2)
    img1xdest = ((img1xsize2 * -1) // 2) + (avatarpix // 2)
    img1ydest = (img1ysize2 * -1) + (avatarpix * 2) + avatarpix

    img3xdest = (screenx // 2) - (avatarpix // 2) + followerx
    img3ydest = (screeny // 2) - (avatarpix // 2) + followery

    # 画像を描画
    # ---------------  1.画像を読み込む  --------------------------

    # 一部の色を透明にする
    img2 = pygame.image.load("avatar/avatar200.png").convert()
    colorkey = img2.get_at((0, 0))
    # colorkey = (255, 255, 255)
    img2.set_colorkey(colorkey, RLEACCEL)

    # 画像の大きさを変える
    img3 = pygame.image.load("avatar/follower200.png").convert()
    colorkey = img3.get_at((0, 0))
    # colorkey = (255, 255, 255)
    img3.set_colorkey(colorkey, RLEACCEL)

    running = True
    # メインループ
    while running:
        screen.fill((0, 0, 0))  # 画面を黒で塗りつぶす

        # ---------------  2.画像を表示  --------------------------
        screen.blit(img1, dest=(img1xdest, img1ydest))
        if img2ydest < img3ydest:
            screen.blit(img2, dest=(img2xdest, img2ydest))
            screen.blit(img3, dest=(img3xdest, img3ydest))
        else:
            screen.blit(img3, dest=(img3xdest, img3ydest))
            screen.blit(img2, dest=(img2xdest, img2ydest))

        pygame.display.update()  # 描画処理を実行
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LSHIFT]:
            speed = defspeed * 2.5
        else:
            speed = defspeed

        if pressed_key[K_LEFT]:
            img1xdest = img1xdest + speed
            if followerx < followermax:
                followerx = followerx + speed
        if pressed_key[K_RIGHT]:
            img1xdest = img1xdest - speed
            if followerx > followermin:
                followerx = followerx - speed
        if pressed_key[K_UP]:
            img1ydest = img1ydest + speed
            if followery < followermax:
                followery = followery + speed
        if pressed_key[K_DOWN]:
            img1ydest = img1ydest - speed
            if followery > followermin:
                followery = followery - speed

        img3xdest = (screenx // 2) - (avatarpix // 2) + followerx
        img3ydest = (screeny // 2) - (avatarpix // 2) + followery

        for event in pygame.event.get():
            # キーイベント処理(キャラクタ画像の移動)
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()  # pygameのウィンドウを閉じる
                sys.exit()  # システム終了
            if event.type == KEYDOWN:  # キーを押したとき
                # ESCキーならスクリプトを終了
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                else:
                    pass
                    #print("押されたキー = " + pygame.key.name(event.key))
                    #print(img1xdest)
                    #print(img1ydest)

        pygame.display.update()  # 画面更新
        pygame.time.wait(30)  # 更新時間間隔
        screen.fill((0, 20, 0, 0))  # 画面の背景色



if __name__ == "__main__":
    # マルチスレッド
    with ThreadPoolExecutor() as Thread1:
        features = [Thread1.submit(TextArea), Thread1.submit(main)]  # 分けたい処理を配列に格納
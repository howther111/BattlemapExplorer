from pygame.locals import *
import pygame
import sys
import settings
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
import tkinter as ttk
import time

# 初期描画
root = tk.Tk()
root.title("育成ゲーム")
# ウィンドウを中心にする

root.geometry("700x700+350+0")
# frame作成
frame1 = ttk.Frame(master=root, width=700, height=700)
frame1.pack()


def Title():
    # キャンバス準備
    cvTitle = tk.Canvas(frame1, bg="black", height=700, width=700)
    # キャンバス表示
    cvTitle.place(x=0, y=0)
    # Title画

    btnHazime = tk.Button(frame1, text='はじめから', font=("MSゴシック", "16", "bold"), bg='white', width=11, height=2)
    btnHazime.place(x=170, y=550)
    btnTuduki = tk.Button(frame1, text='つづきから', font=("MSゴシック", "16", "bold"), bg='white', width=11, height=2)
    btnTuduki.place(x=380, y=550)

    root.mainloop()  # 表示

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
    pygame.display.set_caption("Battlemap Explorer")  # タイトルを作成
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
        features = [Thread1.submit(Title), Thread1.submit(main)]  # 分けたい処理を配列に格納
        root.mainloop()  # 表示
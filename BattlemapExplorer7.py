import math

from pygame.locals import *
import pygame
import sys
import settings

def main():
    pygame.init()  # Pygameを初期化
    screenx = 1440
    screeny = 810
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
        if pressed_key[K_a] and followerx > followermin:
            followerx = followerx - speed
        if pressed_key[K_d] and followerx < followermax:
            followerx = followerx + speed
        if pressed_key[K_w] and followery > followermin:
            followery = followery - speed
        if pressed_key[K_s] and followery < followermax:
            followery = followery + speed
        if pressed_key[K_q]:
            if followermax > 1:
                followermax = followermax - speed
                followermin = followermin + speed
                if followerx >= followermax:
                    followerx = followermax
                if followerx <= followermin:
                    followerx = followermin
                if followery >= followermax:
                    followery = followermax
                if followery <= followermin:
                    followery = followermin
        if pressed_key[K_e]:
            followermax = followermax + speed
            followermin = followermin - speed
            if followerx == followermax - speed:
                followerx = followermax
            if followerx == followermin + speed:
                followerx = followermin
            if followery == followermax - speed:
                followery = followermax
            if followery == followermin + speed:
                followery = followermin

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
    main()
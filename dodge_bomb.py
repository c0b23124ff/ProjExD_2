import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct):
    """
    こうかとんRect,または,爆弾Rectの画面内外判定用の関数
    引数:こうかとんRect,または,爆弾Rect
    戻り値:横方向の判定結果,縦方向の判定結果(True:画面内/False:画面買い)
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def kk_dic():
    """
    向きに対応する画像の辞書を作成
    戻り値:作成した辞書kk_dict
    """
    kk_imgs = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_dict={"5,0":kk_imgs} #右
    kk_imgs = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0)
    kk_dict["5,5"]=kk_imgs #右下
    kk_imgs = pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 2.0)
    kk_dict["0,5"]=kk_imgs #下
    kk_imgs = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0)
    kk_imgs = pg.transform.flip(kk_imgs, True, False)
    kk_dict["-5,5"]=kk_imgs #左下
    kk_imgs = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_imgs = pg.transform.flip(kk_imgs, True, False)
    kk_dict["-5,0"]=kk_imgs #左
    kk_imgs = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0)
    kk_imgs = pg.transform.flip(kk_imgs, True, False)
    kk_dict["-5,-5"]=kk_imgs #左上
    kk_imgs = pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2.0)
    kk_imgs = pg.transform.flip(kk_imgs, True, False)
    kk_dict["0,-5"]=kk_imgs #上
    kk_imgs = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0)
    kk_dict["5,-5"]=kk_imgs #右上
    return kk_dict


def bd_accs(t):
    """
    加速度のリストを作成
    引数：経過時間min(tmr//500,9)
    戻り値：引数に対応する加速度のリスト
    """
    accs = [a for a in range(1,11)] #加速度のリスト    
    return accs[t]

def bd_imgs(t):
    """
    爆弾のサイズのリストを作成
    引数：経過時間min(tmr//500,9)
    戻り値：引数に対応する爆弾サイズのSurface
    """
    bb_imgs = []
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img, (255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_imgs[t]


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    #黒背景
    bl_img = pg.Surface((1600,900))
    pg.draw.rect(bl_img,(0,0,0),(0,0,1600,900),1)
    bl_img.set_alpha
    bl_rct = bl_img.get_rect()
    bl_rct.center = (0,0)
    #kk_dict={(0,-5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    #(-5,-5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)}
    key_dict={pg.K_UP:(0,-5),pg.K_DOWN:(0,5),pg.K_LEFT:(-5,0),pg.K_RIGHT:(5,0)}
    bd_img = pg.Surface((20,20))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    bd_img.set_colorkey((0,0,0))
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = +5,+5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        #衝突判定
        if kk_rct.colliderect(bd_rct):
            print("Game over")
            screen.blit(bl_img, bl_rct) 
            time.sleep(5.0)
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in key_dict.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                    
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        #screen.blit(kk_img, kk_rct)
        if sum_mv[0] == 0 and sum_mv[1] == 0:
            pass
        else:
            kk_img=kk_dic()[str(-sum_mv[0])+","+str(-sum_mv[1])]
        screen.blit(kk_img, kk_rct)
        #bg aで更新
        avx = vx*bd_accs(min(tmr//500,9))#new
        avy = vy*bd_accs(min(tmr//500,9))#new
        bd_rct.move_ip(avx,avy)
        #screen.blit(bd_img, bd_rct)
        screen.blit(bd_imgs(min(tmr//500,9)),bd_rct)
        yoko, tate = check_bound(bd_rct)
        vx *= 1 if yoko else -1
        vy *= 1 if tate else -1
        #if not yoko: #横にはみ出たら
        #    vx *= -1
        #if not tate:
        #    vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

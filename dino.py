import random, os
import time
seed = int.from_bytes(os.urandom(8), 'big')
random.seed(seed)
# import sys, termios, tty
from pynput import keyboard                             


gmPause=False
gmJump=False
land=15 # row of the land
dino_pos=5 # column of the first pixel of the dino
row_dino=3 # height of the dino
col_dino=3 # width of the dino
row_tree=4            # height of the tree
col_tree=3 # width of the tree
FPS = 30               # 30fps/sec
frame_time = 1 / FPS   # 每帧间隔时间The interval time between frames
frame = 1
row = 20
col = 80
real_col=60

def pause(key):
    '''Pause the game when "esc" is pressed. Resume the game when it is pressed again.'''
    global gmPause
    if key == keyboard.Key.esc: # esc时暂停游戏
        if gmPause==False:
            gmPause=True
        else:
            gmPause=False
    # print(gmPause)
    # global gmJump
    # if key == keyboard.Key.space: # space->jump
    #     if gmJump==False:
    #         gmJump=True

def jump(key):
    '''dino jump when "space" is pressed'''
    global gmJump
    if key == keyboard.Key.space: # space->jump
        if gmJump==False:
            gmJump=True

def key_listener(key):
    pause(key)
    jump(key)

def add_dino(mp,dino_feet):
    ''''''
    dino = [['$' for _ in range(col_dino)] for _ in range(row_dino)]
    mp_bckup= [[' ' for _ in range(col_dino)] for _ in range(row_dino)]
    # print(dino)
    x=0
    y=0
    for i in range(land-row_dino+dino_feet,land+dino_feet):
        for j in range(dino_pos-1,dino_pos+col_dino-1):
            # print(x,y)
            mp_bckup[x][y]=mp[i][j]
            mp[i][j]=dino[x][y]
            y+=1
        y=0
        x+=1
    return mp,mp_bckup

def add_tree(mp):
    ''''''
    tree = [['%' for _ in range(col_tree)] for _ in range(row_tree)]
    # print(dino)
    x=0
    y=0
    for i in range(land-row_tree,land):
        for j in range(col-col_tree-1,col-1):
            # print(x,y)
            mp[i][j]=tree[x][y]
            y+=1
        y=0
        x+=1
    return mp

def erase_dino(mp,mp_bckup,dino_feet ):
    global land, row_dino, col_dino
    x=0
    y=0
    for i in range(land-row_dino+dino_feet,land+dino_feet):
        for j in range(dino_pos-1,dino_pos+col_dino-1):
            mp[i][j]=mp_bckup[x][y]
            y+=1
        y=0
        x+=1
    return mp

def warn_print():
    warning_sign = [
        list("########################################"), 
        list("#                                      #"),
        list("#        ████   WARNING!  ████         #"),
        list("#                                      #"),
        list("########################################")
    ]
    for i in range(0,5):
        for j in range(0,40):   
            print(warning_sign[i][j],end='')
        print()


def print_mp(mp,clock):
    if (clock//1000)%2==0: # at a certain period of time, the world turns upsidedown
        if clock%1000==0 and clock!=0:
            print('Okay now back to normal')
            time.sleep(1)
            print("\033c", end="")
            
        for i in range(0,row):
            for j in range(0,real_col):
                print(mp[i][j],end=' ')
            print()
        if clock%1000==0 and clock!=0:
            time.sleep(1)
    else:
        if clock%1000==0:
            # print('Warning!!!!!!!!!')
            warn_print()
            time.sleep(1)
            print("\033c", end="")
                
        for i in range(0,land):
            print()
        for i in range(land,0,-1):
            for j in range(0,real_col):
                print(mp[i][j],end=' ')
            print()
        if clock%1000==0:
            time.sleep(1)

    
    
    print(clock)
    

def main():
    
    global gmJump,gmPause
        
    listener = keyboard.Listener(on_press=key_listener)
    listener.start() 

    # listener2 = keyboard.Listener(on_press=jump)
    # listener2.start() 

    # initialize mp
    mp = [[' ' for _ in range(col)] for _ in range(row)]
    # for i in range(0,row):
    #     mp[i][0]='#'
    for j in range(0,col):# add land
        mp[land][j]='-'
    # print(len(mp))
    # start the game
    x=0
    y=0
    clock=0
    last_tree=-100
    cnt_tree=0
    dino_feet=0
    dino_time=0
    while 1:
        clock+=1
        
        # print(dino_pos )
        if gmJump==True:
            dino_time+=1
            if dino_time<10:
                dino_feet-=1
            else:
                dino_feet+=1
            
            if dino_time==19:
                dino_time=0
                gmJump=False
                dino_feet=0
            
        # start modify the map

        # add the dino to the map
        mp,mp_bckup=add_dino(mp,dino_feet)
        
        # randomly add the tree
        if (clock%random.randint(40, 50)==0 and clock-last_tree>=min(20+cnt_tree/5,50) or clock-last_tree>=60):
            mp=add_tree(mp)
            last_tree=clock
            cnt_tree+=1

        # stop modify the map
        # outprint the game window
        print_mp(mp,clock)

        # erase the dino so it won't roll with the background
        mp=erase_dino(mp,mp_bckup,dino_feet)
        
        for i in range(row):
            if mp[i][0]=='%': # erase the tree
                mp[i][0]=' '
            mp[i] = mp[i][1:] + mp[i][:1] # background rolling

        # 等待下一帧
        time.sleep(max(0.017,0.05/(1+cnt_tree/6)))

        print("\033c", end="")
        
        while gmPause==True:
            # pause_print()
            mp,mp_bckup=add_dino(mp,dino_feet)
            
            print_mp(mp,clock)

            mp=erase_dino(mp,mp_bckup,dino_feet)

            time.sleep(0.1) 
            print("\033c", end="")
        # print(gmPause)



    listener.stop()
    # listener2.stop()


if __name__=='__main__':
    main()
import random, os
import time
from PIL import Image as PILImage
last_time=time.time()
speed=5

seed = int.from_bytes(os.urandom(8), 'big')
random.seed(seed)
# import sys, termios, tty
from graphics import *                      

extra_life=2
gmPause=False
gmDeath=False
gmJump=False
land=150 # row of the land
dino_pos=50 # column of the first pixel of the dino
# row_dino=30 # height of the dino
# col_dino=30 # width of the dino
# row_tree=50 # height of the tree
# col_tree=25 # width of the tree

frame = 1
row = 200
col = 800
real_col=600

dino_feet=0
win = None
grace_period=0

def pause():
    global gmPause
    pause_time=0
    while gmPause==1:
        pause_time+=0.1
        key = win.checkKey()
        if key=='Escape':
            gmPause=0
        time.sleep(0.1) 
    return pause_time
    
def add_tree(trees):
    tree_files = ["tree1.png", "tree2.png", "tree3.png", "tree4.png","tree11.png", "tree12.png", "tree13.png", "tree14.png","tree21.png"]
    chosen_file = random.choice(tree_files)
    global col,land
    # col_tree,row_tree
    img = PILImage.open(chosen_file).convert("RGBA")
    # img = img.resize((col_tree, row_tree))  # 例如 (60, 60)
    temp_name = f"tree_temp_{random.randint(0,10)}.png"
    img.save(temp_name)
    col_tree,row_tree=img.size
    tree_y=(land-row_tree/2)  
    tree_x=(col-(col_tree/2)-1)
    tree_img=Image(Point(tree_x, tree_y), temp_name)
    tree_img.draw(win)
    trees.append((tree_img, img, col_tree, row_tree))
    # print(dino_y," ",dino_x," ",land)
  
def dino_death(dino_img, w1, h1, tree_img, tree_pil, w2, h2):
    """像素级碰撞检测"""
    x1,y1=dino_img.getAnchor().getX(),dino_img.getAnchor().getY()
    x2,y2=tree_img.getAnchor().getX(),tree_img.getAnchor().getY()

    # calculate the bound overlap
    left1,right1=x1-w1/2,x1+w1/2
    top1,bottom1=y1-h1/2,y1+h1/2
    left2,right2=x2-w2/2,x2+w2/2
    top2,bottom2=y2-h2/2,y2+h2/2

    if right1<left2 or right2<left1 or bottom1<top2 or bottom2<top1:
        return False

    # calculate the potential coordinate of overlapping area
    overlap_left=int(max(left1,left2))
    overlap_right=int(min(right1,right2))
    overlap_top=int(max(top1,top2))
    overlap_bottom=int(min(bottom1,bottom2))

    if overlap_right<=overlap_left or overlap_bottom<=overlap_top:
        return False

    # compare the pixel info of dino and tree
    dino_pil=PILImage.open("dino_small.png").convert("RGBA")

    for y in range(overlap_top,overlap_bottom):
        for x in range(overlap_left,overlap_right):
            # the relative coordinate of the pixel in the two images
            dx=int(x-(x1-w1/2))
            dy=int(y-(y1-h1/2))
            tx=int(x-(x2-w2/2))
            ty=int(y-(y2-h2/2))

            # make sure it's legal postion
            if not (0<=dx<w1 and 0<=dy<h1 and 0<=tx<w2 and 0<=ty<h2):
                continue

            # get the transparency of the pixel in each images
            da=dino_pil.getpixel((dx,dy))[3]
            ta=tree_pil.getpixel((tx,ty))[3]

            if da>0 and ta>0:  # not transparent for both
                return True  
    return False

def death_win(win):
    global gmDeath,grace_period,extra_life
    pause_time=0

    rect,wasted_text,info_text,resume=show_wasted(win,extra_life)
    extra_life-=1
    rect.draw(win)
    wasted_text.draw(win)
    info_text.draw(win)
    resume.draw(win)

    while gmDeath==1:
        pause_time+=0.1
        key = win.checkKey()
        if key=='Return':
            gmDeath=0
            break
        
        time.sleep(0.1) 
    grace_period=50

    rect.undraw()
    wasted_text.undraw()
    info_text.undraw()
    resume.undraw()

    return pause_time

def show_wasted(win,extra_life):
    width=win.width
    height=win.height

    # background rectangle
    rect=Rectangle(Point(width/2-150,height/2-60),
                    Point(width/2+150,height/2+60))
    rect.setFill(color_rgb(30,30,30))  # dark gray
    rect.setOutline("red")
    rect.setWidth(3)

    # “WASTED”
    wasted_text=Text(Point(width/2,height/2-20),"WASTED")
    wasted_text.setSize(24)
    wasted_text.setTextColor("red")
    wasted_text.setStyle("bold")
        
    # “Extra Life”
    info_text=Text(Point(width/2,height/2+10), f"Extra Life: {extra_life}")
    info_text.setSize(16)
    info_text.setTextColor("white")

    resume=Text(Point(width/2,height/2+35), f"Press Enter to resume.")
    resume.setSize(9)
    resume.setTextColor("white") 
    return rect,wasted_text,info_text,resume

def main():
    global gmJump,gmPause,gmDeath,win,last_time,grace_period

    win=GraphWin("2D Array Animation", col, row)
    win.setBackground("white")

    # draw the dinosaur
    img=PILImage.open("dino.png").convert("RGBA")
    # img = img.resize((col_dino, row_dino))  # 例如 (60, 60)
    img.save("dino_small.png") 
    col_dino,row_dino=img.size
    dino_y=(land-row_dino/2) 
    dino_x=(dino_pos+col_dino/2-1)
    dino_img=Image(Point(dino_x, dino_y), "dino_small.png")
    dino_img.draw(win)
    # print(dino_y," ",dino_x," ",land)

    # img = PILImage.open(chosen_file).convert("RGBA")
    # # img = img.resize((col_tree, row_tree))  # 例如 (60, 60)
    # temp_name = f"tree_temp_{random.randint(0,9999)}.png"
    # tree_y = (land-row_tree/2)  
    # tree_x = (col-(col_tree/2)-1)
    # tree_img = Image(Point(tree_x, tree_y), temp_name)
    # tree_img.draw(win)
    
    # draw the land
    ground_y=land 
    ground_line=Line(Point(0,ground_y),Point(col,ground_y))
    ground_line.setFill("black")
    ground_line.draw(win)


    x=0
    y=0
    clock=0
    last_tree=-100
    cnt_tree=0
    dino_time=0
    trees = []
    dino_speed=0
    g=0
    first_tree=0
    pause_time=0
    tree_speed=0
    i=0
    while win.checkMouse() is None :
        i+=1
         # update the moving distance with real_time - pause_time, otherwise the tree will suddenly disappear after pausing
        now=time.time()-pause_time
        dt=now-last_time # calculate the time period between two prints
        last_time=now # record the new output timestamp 
        # if tree_speed!=15:
        clock+=1    
        tree_speed=min(5+0.010*clock,15)
        # print(clock," ",tree_speed," ",g," ",dino_speed)
        
        # =============== randomly add the tree ================
        if ((clock%random.randint(40, 50)==0 and clock-last_tree>=min(25+cnt_tree/5,50) or clock-last_tree>=60)):
            add_tree(trees)
            last_tree=clock
            cnt_tree+=1
        
        # =================== python sleep =============== 

        fps=max(0,1/60-(time.time()-now-pause_time))
        time.sleep(fps)
        
        # ========== pause when 'esc' is inputed ===========      
        key=win.checkKey()
        if key=='Escape':
            gmPause=1
            pause_time+=pause()

        # =========== jump when 'space' is inputed ========= 
        dino_feet=dino_img.getAnchor().getY()+(row_dino)/2

        if gmJump==1 and dino_feet==land:
            gmJump=0
            g=0 
        elif gmJump==0 and key=='space':
            gmJump=1
            g=3
            dino_speed=-24
            # print("%%%")
        # print()

        dino_speed+=g
        print(dino_speed," ",dino_feet)
        if gmJump==1:
            dino_dx=(dino_speed)
            dino_img.move(0,dino_dx)
            print(dino_dx)
            # dino_speed+=g*dt
        
        # ========= check whether the dinosaur died ========= 
        print(grace_period)
        if len(trees)>0:
            tree_img, tree_pli, col_tree, row_tree = trees[0]
            if grace_period==0 and dino_death(dino_img,col_dino,row_dino,tree_img,tree_pli,col_tree,row_tree):
                gmDeath=1
                # print("%%%%%%%%%%%%%%%%%%%")
                death_win(win)
                if extra_life==-1:
                    break
        if grace_period>0: 
            if grace_period%10==0:
                dino_img.undraw()
            elif grace_period%10==5:
                dino_img.draw(win)
            grace_period-=1

        # =============== move the trees =============== 
        
        tree_dx=-tree_speed*dt*60   # 以 60fps 标准化速度
        for tree_img, tree_pli, col_tree, row_tree in trees:
            tree_img.move(tree_dx,0)
            if tree_img.getAnchor().getX()+30<-col_tree:
                trees.remove((tree_img, tree_pli, col_tree, row_tree))

        # =============== print the score ===============
    win.close()

if __name__=='__main__':
    main()


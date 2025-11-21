import random, os
import time
from PIL import Image as PILImage
last_time=time.time()
speed=5

seed = int.from_bytes(os.urandom(8), 'big')
random.seed(seed)
# import sys, termios, tty
from graphics import *                      

dino_x=0
dino_y=0
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


img=PILImage.open("dino0.png").convert("RGBA")
img1=PILImage.open("dino1.png").convert("RGBA")
img2=PILImage.open("dino2.png").convert("RGBA")
    # img = img.resize((col_dino, row_dino))  # 例如 (60, 60)
img.save("dino_small.png") 
img1.save("dino_small1.png") 
img2.save("dino_small2.png") 

dino_img=Image(Point(dino_x, dino_y), "dino_small.png")
dino_img1=Image(Point(dino_x, dino_y), "dino_small1.png")
dino_img2=Image(Point(dino_x, dino_y), "dino_small2.png")

def restart_program():
    """restart the current program, with file objects and descriptors"""
    

    python = sys.executable
    os.execl(python, python, *sys.argv)

def save_score(clock):
    """this is where the highest score is saved
        clock-1 = current score """
    highest_score = open("high_score.txt", "r")
    high_score_num = highest_score.read()

    highest_score = open("high_score.txt", "w")
    highest_score.write (str(max(int(high_score_num),clock-1))) 
    highest_score.close()

def pause(clock):
    """ when the game is paused, the game goes to "sleep" and the menu pops up """
    global gmPause #game is running with all graphics if pause time is 0 (so R key has not been pressed)
    pause_time=0
    rect,menu_text,info_text,score,resume,retry,rank=print_menu(clock)
    rect.draw(win)
    menu_text.draw(win)
    info_text.draw(win)
    score.draw(win)
    resume.draw(win)
    retry.draw(win)
    rank.draw(win)


    while gmPause==1: #while the game is not paused
        pause_time+=0.1 #this makes sure that the trees are stationary until the R key is pressed to unpause the game
        key = win.checkKey() #this just makes it easier to read that the function win.checkKey is being checked for
        if key=='r' or key=='R': #R key pressed AGAIN, then the game continues.
            save_score(clock)
            restart_program()
        if key=='a'or key=='A':
            ranking(clock)
        if key=='Escape':
            gmPause=0
        time.sleep(0.1) 
    rect.undraw()
    menu_text.undraw()
    info_text.undraw()
    score.undraw()
    resume.undraw()
    retry.undraw()
    rank.undraw()
    return pause_time
    
def add_tree(trees):
    """the system will randomly select trees to pop up"""
    tree_files = ["tree1.png", "tree2.png", "tree3.png", "tree4.png","tree11.png", "tree12.png", "tree13.png", "tree14.png","tree21.png"]
    chosen_file = random.choice(tree_files)
    global col,land
    # col_tree,row_tree
    img = PILImage.open(chosen_file).convert("RGBA") #converts the format of the tree file to have transparent background recognized
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
    """ this system checks when the dinosaur and a tree overlaps and if they do
        overlap generally (by length and width of their image) and the system
        wont count for the transparent pixels that do overlap"""
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

def death_win(win,clock):
    """ there's a while loop that checks for the player's keyboard input,
        if they select return the game starts again
        if they selet 'r'/'R' the game restarts
        otherwise the wasted menu stays on the screen """
    global gmDeath,grace_period,extra_life
    pause_time=0

    rect,wasted_text,info_text,score,resume,retry,rank=show_wasted(win,extra_life,clock)
    extra_life-=1
    rect.draw(win)
    wasted_text.draw(win)
    info_text.draw(win)
    score.draw(win)
    resume.draw(win)
    retry.draw(win)
    rank.draw(win)

    while gmDeath==1:
        pause_time+=0.1
        key = win.checkKey()
        if key=='Return':
            gmDeath=0
            break
        if key=='r' or key=='R':
            save_score(clock)
            restart_program()
        if key=='a'or key=='A':
            ranking(clock)
        
        time.sleep(0.1) 
    grace_period=40

    rect.undraw()
    wasted_text.undraw()
    info_text.undraw()
    score.undraw()
    resume.undraw()
    retry.undraw()
    rank.undraw()

    return pause_time

def show_wasted(win,extra_life,clock):
    """ defines the wasted window (the font, coloring, size) """
    width=win.width
    height=win.height

    # background rectangle
    rect=Rectangle(Point(width/2-150,height/2-80),
                    Point(width/2+150,height/2+80))
    rect.setFill(color_rgb(30,30,30))  # dark gray
    rect.setOutline("red")
    rect.setWidth(3)

    # “WASTED”
    wasted_text=Text(Point(width/2,height/2-40),"WASTED")
    wasted_text.setSize(24)
    wasted_text.setTextColor("red")
    wasted_text.setFace("courier")  
    wasted_text.setStyle("bold")
        
    # “Extra Life”
    info_text=Text(Point(width/2,height/2-10), f"Extra Life: {extra_life}")
    info_text.setSize(16)
    info_text.setFace("courier")  
    info_text.setTextColor("white")

    score=Text(Point(width/2,height/2+10), f"Score: {clock-1}")
    score.setSize(16)
    score.setFace("courier")  
    score.setTextColor("white")

    resume=Text(Point(width/2,height/2+30), f"Press Return to resume.")
    resume.setSize(9)
    resume.setFace("courier")  
    resume.setTextColor("white") 

    retry=Text(Point(width/2,height/2+40), f"Press R to restart.")
    retry.setSize(9)
    retry.setFace("courier")  
    retry.setTextColor("white") 

    rank=Text(Point(width/2,height/2+50), f"Press A to see your ranking.")
    rank.setSize(9)
    rank.setFace("courier")  
    rank.setTextColor("white") 
    return rect,wasted_text,info_text,score,resume,retry,rank

def print_menu(clock):
    """ defines the pause window (the font, coloring, size) """
    width=win.width
    height=win.height

    # background rectangle
    rect=Rectangle(Point(width/2-120,height/2-80),
                    Point(width/2+120,height/2+80))
    rect.setFill(color_rgb(30,30,30))  # dark gray
    rect.setOutline("green")
    rect.setWidth(3)

    # “MENU”
    menu_text=Text(Point(width/2,height/2-40),"MENU")
    menu_text.setSize(24)
    menu_text.setTextColor("green")
    menu_text.setFace("courier")  
    menu_text.setStyle("bold")

    # “Extra Life”
    info_text=Text(Point(width/2,height/2-15), f"Remaining Life: {extra_life+1}")
    info_text.setSize(16)
    info_text.setFace("courier")  
    info_text.setTextColor("white")

    score=Text(Point(width/2,height/2+5), f"Score: {clock-1}")
    score.setSize(16)
    score.setFace("courier")  
    score.setTextColor("white")


    resume=Text(Point(width/2,height/2+30), f"Press Esc to resume.")
    resume.setSize(9)
    resume.setFace("courier")  
    resume.setTextColor("white") 

    retry=Text(Point(width/2,height/2+40), f"Press R to restart.")
    retry.setSize(9)
    retry.setFace("courier")  
    retry.setTextColor("white") 

    rank=Text(Point(width/2,height/2+50), f"Press A to see your ranking.")
    rank.setSize(9)
    rank.setFace("courier")  
    rank.setTextColor("white") 

    return rect,menu_text,info_text,score,resume,retry,rank

    # print(contents)

def update_dino(clock):
    """ the movement of the dinosuar
         when the clock is odd, left leg is up
         when the clock is even, right led is up """
    global dino_x,dino_y,dino_img
    if 1:
        if clock%2==1:
            dino_nxt=Image(Point(dino_x, dino_y), "dino_small1.png")
            dino_nxt.draw(win)
            dino_img.undraw()
            dino_img=dino_nxt
        else:
            dino_nxt=Image(Point(dino_x, dino_y), "dino_small2.png")
            dino_nxt.draw(win)
            dino_img.undraw()
            dino_img=dino_nxt

def ranking(clock):
    """ this function is to show the ranking of the players based on their highest scores
        it reads from the high_score.txt file and sorts the scores in descending order
        then it displays the top 5 scores on the screen """
    ranking = []
    highest_score = open("high_score.txt", "r")
    high_score_num = highest_score.read()
    with open("ranking.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                id_, score = parts
                ranking.append((id_, int(score)))
    ranking.append(("You", max(int(high_score_num),clock-1)))
    ranking.sort(key=lambda x: x[1], reverse=True)


    width=win.width
    height=win.height

    # background rectangle
    rect=Rectangle(Point(width/2-180,height/2-80),
                    Point(width/2+180,height/2+80))
    rect.setFill(color_rgb(30,30,30))  # dark gray
    rect.setOutline("red")
    rect.setWidth(3)
    rect.draw(win)

    
    # “WASTED”
    rank_text=Text(Point(width/2,height/2-50),"Global Rank")
    rank_text.setSize(24)
    rank_text.setTextColor("red")
    rank_text.setFace("courier")  
    rank_text.setStyle("bold")
    rank_text.draw(win)
    rank_list = []
    num=['1st','2nd','3rd','4th','5th']
    for i in range(len(ranking)):
        if i>=5:
            break
        id_, score = ranking[i]
        rank_entry = Text(Point(width/2, height/2 - 25 + i*20), f"{num[i]:4} {id_:10}: {score:10}")
        rank_list.append(rank_entry)
        rank_entry.setSize(16)
        rank_entry.setTextColor("white")
        rank_entry.setFace("courier")
        rank_entry.draw(win)
    while True:
        key = win.checkKey()
        if key=='a' or key=='A':
            break
    for r in rank_list:
        r.undraw()
    rect.undraw()
    rank_text.undraw()

def main():
    """ there's a big while loop, the system sleeps for every transversal
        allowing the users to have their eye adjusted to the updates on the screen
        Every transversal there's an update for every function (trees, dinosaur, pause/death screens, and jump)"""

    global gmJump,gmPause,gmDeath,win,last_time,grace_period,dino_x,dino_y,dino_img

    win=GraphWin("2D Array Animation", col, row)
    win.setBackground("white")


    # =============== initial output ================
    # ============draw the dinosaur=========
    
    col_dino,row_dino=img.size
    dino_y=(land-row_dino/2) 
    dino_x=(dino_pos+col_dino/2-1)
    dino_img.draw(win)
    # print(dino_y," ",dino_x," ",land)
    
    # =============draw the land==========
    ground_y=land 
    ground_line=Line(Point(0,ground_y),Point(col,ground_y))
    ground_line.setFill("black")
    ground_line.draw(win)

    # =============initialization of variables==========
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
    
    # =============print current score==========
    current_score = Text(Point(120, 20), f"current score:{clock}")  # 初始文字
    current_score.setSize(16)
    current_score.draw(win)
    current_score.setFace("courier")  

    # =============get and print highest score==========
    highest_score= open("high_score.txt", "r")
    high_score_num = highest_score.read()
    highest_score.close()
    high_score = Text(Point(520, 20), f"highest score:{high_score_num}")  # 初始文字
    high_score.setSize(16)
    high_score.draw(win)
    high_score.setFace("courier")  

    while win.checkMouse() is None :
        current_score.setText(f"current score: {clock}")
        high_score_num = max(int(high_score_num),clock)
        high_score.setText(f"highest score:{high_score_num}")
        # update_dino(clock)
        

        i+=1
         # update the moving distance with real_time - pause_time, otherwise the tree will suddenly disappear after pausing
        now=time.time()-pause_time
        dt=now-last_time # calculate the time period between two prints
        last_time=now # record the new output timestamp 
        # if tree_speed!=15:
        clock+=1    
        tree_speed=min(5+0.010*clock,15)

        save_score(clock)
        # print(clock," ",tree_speed," ",g," ",dino_speed)
        
        # =============== randomly add the tree ================
        if ((clock-last_tree>=random.randint(10,15) or clock-last_tree>=30)):
            add_tree(trees)
            last_tree=clock
            cnt_tree+=1
        
        # =================== python sleep =============== 

        fps=max(0,1/15-(time.time()-now-pause_time))
        time.sleep(fps)
        
        # ========== pause when 'esc' is inputed ===========      
        key=win.checkKey()
        if key=='Escape':
            gmPause=1
            pause_time+=pause(clock)

        # =========== jump when 'space' is inputed ========= 
        dino_feet=dino_img.getAnchor().getY()+(row_dino)/2

        if gmJump==1 and dino_feet==land:
            gmJump=0
            g=0 
        elif gmJump==0 and key=='space':
            # grace_period=0
            gmJump=1
            g=10
            dino_speed=-40
            # print("%%%")
        # print()
        dino_speed+=g
        # print(dino_speed," ",dino_feet)
        if gmJump==1:
            dino_dx=(dino_speed)
            dino_y+=dino_dx
            dino_img.move(0,dino_dx)
            # print(dino_dx)
            # dino_speed+=g*dt
        # =============== move the trees =============== 
        
        # print(tree_speed)
        tree_dx=-tree_speed*dt*60   # 以 60fps 标准化速度
        for tree_img, tree_pli, col_tree, row_tree in trees:
            tree_img.move(tree_dx,0)
            if tree_img.getAnchor().getX()+30<-col_tree:
                trees.remove((tree_img, tree_pli, col_tree, row_tree))

        # ========= check whether the dinosaur died ========= 
        # print(grace_period)
        if len(trees)>0:
            tree_img, tree_pli, col_tree, row_tree = trees[0]
            if grace_period==0 and dino_death(dino_img,col_dino,row_dino,tree_img,tree_pli,col_tree,row_tree):
                gmDeath=1
                # print("%%%%%%%%%%%%%%%%%%%")
                death_win(win,clock)
                if extra_life==-1:
                    break


        # =============== update the dinosaur ===============
        
        if grace_period==0:
            update_dino(clock)
        elif grace_period>0: 
            if grace_period%4==0:
                dino_nxt=Image(Point(dino_x, dino_y), "dino_trans.png")
                dino_nxt.draw(win)
                dino_img.undraw()
                dino_img=dino_nxt
            elif grace_period%4==2:
                if clock%2==0:
                    dino_nxt=Image(Point(dino_x, dino_y), "dino_small2.png")
                else:
                    dino_nxt=Image(Point(dino_x, dino_y), "dino_small1.png")
                dino_nxt.draw(win)
                dino_img.undraw()
                dino_img=dino_nxt
            elif grace_period%4<2:
                update_dino(clock)
            grace_period-=1
        

        
        # =============== record the score ===============
    
    
    win.close()   
    save_score(clock)

if __name__=='__main__':
    main()
# Dinosaur - csc110 final project

# Team Members

Tensae Mekonnen, Mandy Mi, Elizabeth Sarpong

# Required Files

All files contained in the Dinosaur Repository besides the README.md are required.  Must install a pillow by running pip install pillow to allow transparent pixel recognition. Additionally, the Pygame package must be installed by running pip install pygame to play sound effects and background music. Pillow is a fork of the Python Imaging Library that allows us to display images with transparent backgrounds using the Image.convert(“RGBA”). We also use Pillow to process images that are transparent using the Image.Draw() function and the undraw function. Pygame is a package that includes modules, of which we utilize the pygame.mixer.sound and pygame.mixer.music functions to play sound effects and background music, respectively. The picture files including dino, dino0, din01, and dino2 are used to simulate the dinosaur running. Users must select the right python file to run, depending on the operating system of the computer. If you’re a windows user run ( dino_win_ver_1.0.py). If you're a mac user run (dino_mac_ver_1.0.py). 

# How to Run
 
First load into game 

- The game starts, background music starts playing!
  - User spawns in with 3 lives initially 
  - Player must press spacebar to avoid oncoming obstacles
  - Game initially starts off slow but speeds up as time/score increases

User presses esc: 

- Game Pauses
  - Menu screen appears with instructions
  - To get out of this screen user must press esc 

User presses R/r: 

- Game restarts with RENEWED lives 
  - Spawn in immediately and press spacebar to avoid oncoming obstacles
  - Game initially starts off slow but speeds up as time/score increases
 
User presses A/a:

- Scoreboard appears
  - Shows the users score listed in descending order
  - Compared to 4 other highest scorers (developers of the game)
  - To get out of this screen user must press A/a

User presses space:

- Dinosaur jumps, and the jump sound effect plays.

User hits an obstacle:

- Wasted screen appears with instructions
- To get out of this screen user must press return

User presses return:

- Game restarts with REMAINING lives
  - Spawn in immediately and press spacebar to avoid oncoming obstacles
  - Game initially starts off slow but speeds up as time/score increases

User runs out of lives:

- Game is over 
  - Wasted screen appears with instructions
  - The background music stops, and death sound effect plays.
  - To get out of this screen user must press return.
  - To restart, press R/r
  - To see scoreboard, press A/a
  - User's highest score across all three attempts will be saved, even if the window is closed and reopened

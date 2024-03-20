import pygame
import math
import sys
import random
from pygame.locals import*
from pygame import mixer
#initialize the pygame
pygame.init()
#create the screen
screen=pygame.display.set_mode((800,600))
#background
background=pygame.image.load('Space Invaders Game[Items]/Space background.png')
#background sound
mixer.music.load('Space Invaders Game[Items]/background.wav')
mixer.music.play(-1)
#title(caption) and icon
pygame.display.set_caption("Space Invaders By Shreshth Srivastava")
icon = pygame.image.load('Space Invaders Game[Items]/ufo.png')
pygame.display.set_icon(icon)
#Title
Title=pygame.image.load('Space Invaders Game[Items]/Title.png')
#Numbers
Game_Sprites={}
Game_Sprites['Numbers']=(
    pygame.image.load('Space Invaders Game[Items]/0.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/1.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/2.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/3.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/4.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/5.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/6.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/7.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/8.png').convert_alpha(),
    pygame.image.load('Space Invaders Game[Items]/9.png').convert_alpha(),
    )
#Score
Score=pygame.image.load('Space Invaders Game[Items]/Score.png').convert_alpha()
#player
playerimg=pygame.image.load('Space Invaders Game[Items]/player.png')
playerX=370
playerY=480
playerX_change=0
#enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
enemy_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('Space Invaders Game[Items]/enemy2.png'))
    enemyX.append(random.randint(0,700))
    enemyY.append(random.randint(40,100))
    enemyX_change.append(6)
    enemyY_change.append(30)
#bullet
#ready state means you can't see the bullet on the screen
#fire means that the bullet is currently moving
bulletimg=pygame.image.load('Space Invaders Game[Items]/bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bullet_change=30
bullet_state="ready"
#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
#game over text
def show_score(x,y):
    myDigits=[int(x) for x in list(str(score_value))]
    width=0
    for digit in myDigits:
        width+=Game_Sprites['Numbers'][digit].get_width()
        Xoffset=((470-width)/4)+100
        for digit in myDigits:
            screen.blit(Score,(0,0))
            screen.blit(Game_Sprites['Numbers'][digit],(Xoffset-100,12))
            Xoffset+=(Game_Sprites['Numbers'][digit].get_width())*1.5
            pygame.display.update()
def game_over_text():
    over_text=pygame.image.load('Space Invaders Game[Items]/Gameover.png')
    screen.blit(over_text,(325,225))
def player(x,y):
    screen.blit(playerimg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+34,y+10))
def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False
def welcomescreen():
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button,close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if the user presses space or up key,start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                screen.blit(background,(0,0))
                screen.blit(playerimg,(370,480))
                screen.blit(Title,(150,0))
                fpsClock=pygame.time.Clock()
                pygame.display.update()
                fpsClock.tick(60)
welcomescreen()
#game loop
running=True
while running:
    #RGB=Red,Green,Blue
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT or(event.type==KEYDOWN and event.key==K_ESCAPE):
            running=False
            quit()
        #if keystroke is pressed check whether its right or len
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-15
            if event.key==pygame.K_RIGHT:
                playerX_change=15
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound('Space Invaders Game[Items]/laser.wav')
                    bullet_sound.play()
                    #get the current x coordinate of the spaceship
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)    
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
    #5+=5+(-1)=5-1=4
    #5+=5+1=6
    #checking for boundaries for spaceship so it doesn't go out of boundary
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=700:
        playerX=700
    #enemy movement
    for i in range(num_of_enemies):
        #game over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            bullet_state='not ready'
            break
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=700:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
        #collision
        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound('Space Invaders Game[Items]/explosion.wav')
            explosion_sound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,700)
            enemyY[i]=random.randint(40,100)
        enemy(enemyX[i],enemyY[i],i)
    fpsClock=pygame.time.Clock()
    #bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bullet_change
    player(playerX,playerY)
    show_score(textX,textY)
    fpsClock.tick(120)
    pygame.display.update()
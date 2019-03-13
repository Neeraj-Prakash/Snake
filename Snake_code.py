#!/usr/bin/python3

import pygame
import time
import random

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (180,0,0)
b_red = (255,0,0)
green = (0,180,0)
b_green = (0,255,0)
blue = (0,0,255)
b_blue = (24,200,231)

game_width = 800
game_height = 600
block_size = 20
block_speed = 1
clock = pygame.time.Clock()
FPS = 5
direction = "right"

img = pygame.image.load('./snkHead.png')
appleImg = pygame.image.load('./appleImg.png')
icon = pygame.image.load('./gameIcon.png')

gameDisplay = pygame.display.set_mode((game_width,game_height))
pygame.display.set_caption('Snake')
pygame.display.set_icon(icon)

smallfont = pygame.font.SysFont('Elephant', 25)
medfont = pygame.font.SysFont('Calibri', 50)
largefont = pygame.font.SysFont('Forte', 80)

def snake(block_size,snakelist):
    if direction == "right":
        head = pygame.transform.rotate(img,270)
    if direction == "left":
        head = pygame.transform.rotate(img,90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img,180)
    
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size-1,block_size-1])

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(msg,color,displace = 0,size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (game_width/2), (game_height/2) + displace
    gameDisplay.blit(textSurf, textRect)

def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    appleX = round(random.randrange(250, game_width - block_size)/block_size)*block_size
    appleY = round(random.randrange(30, game_height - block_size)/block_size)*block_size
    return appleX, appleY

def pause():
    paused = True
    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pygame.mixer.music.unpause()
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_display("Paused",
                        b_red,
                        -100,
                        size = "large")
        message_display("Press C to continue or Q to quit",
                        black,
                        10,
                        size = "medium")
        pygame.display.update()
        clock.tick(5)

def gameIntro():
    intro = True



    while intro:
        gameDisplay.fill(white)
        message_display("Welcome to Slither",
                        b_red,
                        -100,
                        "large")
        message_display("- Eat as much apples as you can",
                        blue,
                        -10,
                        "medium")
        message_display("- Use arrow keys to move around",
                        blue,
                        40,
                        "medium")
        message_display("Press C to play or Q to quit",
                        black,
                        120,
                        "medium")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    gameLoop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(15)

def gameLoop():
    global direction
    snakeLength = 1
    snakeList = []
    gameExit = False
    gameOver = False
    lead_x = game_width/2
    lead_y = game_height/2
    lead_x_change = 20
    lead_y_change = 0
    appleX, appleY = randAppleGen()

    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load('.\\back.ogg')
    pygame.mixer.music.play(-1)
    
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            message_display("Game Over",b_red,-50,size = "large")
            message_display("Press C to play again and Q to quit",
                            black,
                            displace = 20,
                            size="medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                    if event.key == pygame.K_c:
                        direction = "right"
                        gameLoop()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
                            
        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x<0 or lead_x>=game_width-block_size or lead_y<0 or lead_y>=game_height-block_size:
            gameOver = True
            
        gameDisplay.fill(white)
        gameDisplay.blit(appleImg, (appleX, appleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
    
        if len(snakeList) > snakeLength:
            del snakeList[0]

        for segment in snakeList[:-1]:
            if segment == snakeHead:
                gameOver = True
            
        snake(block_size,snakeList)
        score(snakeLength-1)
        pygame.display.update()
        
        if lead_x == appleX and lead_y ==appleY:
            appleX, appleY = randAppleGen()
            snakeLength +=1
        
        clock.tick(FPS)
        
gameIntro()


import pygame
from win32api import GetSystemMetrics
import sys
import random

screenWidth = GetSystemMetrics(0)
screenHeight = GetSystemMetrics(1)

gray = 82, 82, 82
white = 255, 255, 255
green = 150, 200, 20
blue = 67, 84, 255
orange = 255, 165, 0
red = 250, 0, 0
purple = 172, 79, 198
gray2 = 128, 128, 128

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
clock = pygame.time.Clock()

playerX = 10
playerY = int(screenHeight/2-70)

computerX = screenWidth-20
computerY = int(screenHeight/2-70)

#random_obstacleX = int(screenWidth/2)
random_obstacleX = -10
random_obstacleY = 0

ball = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
ballStart = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)

gameStart = False

ballSpeed_x = 14
ballSpeed_y = 14

ballSpeed_xS = 7
ballSpeed_yS = -7

player_Score = 0
oppenentScore = 0

player2 = False

startScreen = True

cx, cy = 0, 0

current_color = white

difficultyIndicator = 3
difficultyLevel = 'Impossible'

levelUpW = 100
levelUpCount = 100

playerVel = 10
compVel = 0

power_Up = False

obstacleTime = 800
timeOut = 100

paddleHits = 0
multipliHits = 15

left_right = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            cx, cy = pygame.mouse.get_pos()
            print(cx, cy)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and  playerY >= 20:
        playerY -= playerVel
    if keys[pygame.K_s] and playerY <= screenHeight - 20 - 140:
        playerY += playerVel
    if player2 == True:
        if keys[pygame.K_UP] and computerY >= 20:
            computerY -= 10
        if keys[pygame.K_DOWN] and computerY <= screenHeight - 20 - 140:
            computerY += 10
    if keys[pygame.K_SPACE]:
        gameStart = True
    if keys[pygame.K_1]:
        pygame.quit()
        sys.exit()

    screen.fill((30, 30, 30))
    font = pygame.font.SysFont("comicsansms", 50)
    fontBig = pygame.font.SysFont("comicsansms", 75)
    fontSmall = pygame.font.SysFont("comicsansms", 25)

    if startScreen == False:
        player = pygame.draw.rect(screen, current_color, (computerX, computerY, 10, 140))
        Comp = pygame.draw.rect(screen, current_color, (playerX, playerY, 10, 140))
        random_obstacle = pygame.draw.rect(screen, current_color, (random_obstacleX, random_obstacleY, 10, screenHeight))
        #Start game
        if gameStart == False:
            startButton = font.render("Click anywhere on the screen to begin", bool(1), (255, 255, 255))
            screen.blit(startButton, (screenWidth / 2 - 400, screenHeight / 2 - 125))

            if cx > 0 and cx < screenWidth:
                if cy > 50 and cy < screenHeight-75:
                    cx, cy = 0, 0
                    gameStart = True

        if gameStart == True:
            #Ball logic
            ball.x += ballSpeed_x
            ball.y += ballSpeed_y

            if ball.top <= 0 or ball.bottom >= screenHeight:
                ballSpeed_y *= -1
            if ball.left <= 0 or ball.right >= screenWidth:
                ballSpeed_x *= -1

            if ball.x <= 5:
                oppenentScore += 1
                if timeOut <= 1:
                    ball.x = screenWidth / 2 - 15
                    ball.y = screenHeight / 2 - 15
                else:
                    left_right = random.randint(1, 2)
                    if left_right == 1:
                        ball.x = screenWidth / 2 - 200
                        ball.y = screenHeight / 2 - 200
                    if left_right == 2:
                        ball.x = screenWidth / 2 + 200
                        ball.y = screenHeight / 2 + 200
                gameStart = False
            if ball.right >= screenWidth:
                player_Score += 1
                if timeOut <= 1:
                    ball.x = screenWidth / 2 - 15
                    ball.y = screenHeight / 2 - 15
                else:
                    ball.x = screenWidth / 2 - 200
                    ball.y = screenHeight / 2 - 200
                gameStart = False
            #Collision
            if ball.colliderect(player) or ball.colliderect(Comp):
                ballSpeed_x *= -1
                paddleHits += 1
                if paddleHits == multipliHits:
                    multipliHits += 15
                    if ballSpeed_x > 0:
                        ballSpeed_x += 1
                    else:
                        ballSpeed_x -= 1
                    if ballSpeed_y > 0:
                        ballSpeed_y += 1
                    else:
                        ballSpeed_y -= 1

            if ball.colliderect(random_obstacle):
                ballSpeed_x *= -1

            #Comp logic
            if player2 == False:
                if difficultyLevel == 'Easy':
                    compVel = 10
                if difficultyLevel == 'Hard':
                    compVel = 12
                if difficultyLevel == 'Impossible':
                    compVel = 15

                if ball.y > computerY and computerY <= screenHeight - 20 - 140:
                    computerY += compVel
                if ball.y < computerY and computerY >= 20:
                    computerY -= compVel


            #Draw
            pygame.draw.ellipse(screen, current_color, ball)
            pygame.draw.rect(screen, current_color, player)
            pygame.draw.rect(screen, current_color, Comp)
            pygame.draw.rect(screen, current_color, random_obstacle)
            if gameStart == True:
                pygame.draw.line(screen, gray, (screenWidth/2, 0), (screenWidth/2, screenHeight))

            #Draw score
            computerScore = font.render(str(oppenentScore), bool(1), (255, 255, 255))
            screen.blit(computerScore, (screenWidth / 2 + 20, 10))
            playerScore = font.render(str(player_Score), bool(1), (255, 255, 255))
            if player_Score < 10:
                screen.blit(playerScore, (screenWidth / 2 - 50, 10))
            else:
                if player_Score <= 99:
                    screen.blit(playerScore, (screenWidth / 2 - 70, 10))
                else:
                    screen.blit(playerScore, (screenWidth / 2 - 100, 10))

        #Obstacle logic
        if obstacleTime <= 1:
            random_obstacleX = int(screenWidth/2)
            timeOut = random.randint(0, 500)
            if timeOut <= 1:
                obstacleTime = random.randint(500, 1000)
                random_obstacleX = -10
            else:
                timeOut -= 1
        else:
            obstacleTime -= 1

    if startScreen == True:
        ballStart.x += ballSpeed_xS
        ballStart.y += ballSpeed_yS

        if ballStart.top <= 0 or ballStart.bottom >= screenHeight:
            ballSpeed_yS *= -1
        if ballStart.left <= 0 or ballStart.right >= screenWidth:
            ballSpeed_xS *= -1
        print(ballStart.y)
        pygame.draw.ellipse(screen, gray, ballStart)
        TableTennis = fontBig.render("Table Tennis", bool(1), (255, 255, 255))
        screen.blit(TableTennis, (screenWidth / 2 - 225, screenHeight / 2 - 350))
        start = font.render("1 Player - Start - 2 Player", bool(1), (255, 255, 255))
        screen.blit(start, (screenWidth / 2 - 300, screenHeight - 350))
        if cx < screenWidth/2:
            player2 = False
        if cx > screenWidth/2:
            player2 = True
        if cx > 0 and cx < screenWidth:
            if cy > 50 and cy < screenHeight-75:
                cx, cy = 0, 0
                startScreen = False

    if player2 == False:
        difficultyLevelLabel = fontSmall.render(f"Difficulty Level: {difficultyLevel}", bool(1), (255, 255, 255))
        screen.blit(difficultyLevelLabel, (10, 10))
        if cx > 0 and cx < 333:
            if cy > 0 and cy < 49:
                cx, cy = 0, 0
                if difficultyIndicator == 3:
                    difficultyIndicator = 1
                elif difficultyIndicator == 2:
                    difficultyIndicator = 3
                elif difficultyIndicator == 1:
                    difficultyIndicator = 2
                if difficultyIndicator == 1:
                    difficultyLevel = 'Easy'
                if difficultyIndicator == 2:
                    difficultyLevel = 'Hard'
                if difficultyIndicator == 3:
                    difficultyLevel = 'Impossible'

    #Power Up
    if player2 == False:
        if startScreen == False:
            pygame.draw.rect(screen, red, (screenWidth / 1.07, 10, levelUpW, 50))
            if levelUpW <= 1:
                if cx > screenWidth/1.07 and cx < screenWidth:
                    if cy < 50:
                        cx, cy = 0, 0
                        power_Up = True
                        levelUpCount = 100
            else:
                if gameStart == True:
                    levelUpW -= 0.1

            if power_Up == True:
                playerVel = 20
                pygame.draw.rect(screen, blue, (screenWidth / 1.07, 10, levelUpCount, 50))
                if levelUpCount <= 1:
                    levelUpW = 100
                    playerVel = 10
                    current_color = white
                    power_Up = False
                else:
                    levelUpCount -= 0.5
                    current_color = orange

            powerUp = fontSmall.render("Speed", bool(1), (255, 255, 255))
            screen.blit(powerUp, (screenWidth / 1.062, 15))
            pygame.draw.rect(screen, white, pygame.Rect(screenWidth / 1.07, 10, 100, 50), 2, 3)

    # Exit
    exit = font.render("EXIT", bool(1), (255, 255, 255))
    screen.blit(exit, (screenWidth / 1.1, screenHeight - 75))
    if cx > screenWidth / 1.1 and cx < screenWidth:
        if cy > screenHeight - 75 and cy < screenHeight:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
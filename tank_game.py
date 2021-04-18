import pygame
from math import *
import random

pygame.init()
clock = pygame.time.Clock()

FPS = 15
width = 800
height = 600
groundHeight = 527
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tankers")

largeFont = pygame.font.SysFont(None, 60, True)
medFont = pygame.font.SysFont(None, 40)
smallFont = pygame.font.SysFont(None, 30)

msgDict = {"small": smallFont, "medium": medFont, "large": largeFont}

grey = (100, 100, 100)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
green = (0, 255, 0)
inactive_green = (0, 100, 10)

playerHealth = 100
enemyHealth = 100

def text_align(win, text, y_displacement):
    text_rect = text.get_rect(center=(width / 2, (height / 2) + y_displacement))
    win.blit(text, text_rect)

def message(win, msg, color, size, y_displacement):
    text = msgDict[size].render(msg, True, color)
    text_align(win, text, y_displacement)

def button(msg, activeColor, inactiveColor, x, y, msgColor, action, msgSize = "medium"):
        mpos = pygame.mouse.get_pos()
        mclick = pygame.mouse.get_pressed()
        text = msgDict[msgSize].render(msg, True, msgColor)
        text_height = text.get_height()
        text_width = text.get_width()
        active = False
        click = False
        if x - 10 < mpos[0] < x + text_width + 10:
            if y - 10 < mpos[1] < y + text_height + 10:
                active = True
                if mclick[0] == 1:
                    click = True
        if active == True:
            pygame.draw.rect(win, activeColor, [x-10, y-10, text_width+20, text_height+20])
            if click == True:
                action()
        else:
            pygame.draw.rect(win, inactiveColor, [x - 10, y - 10, text_width + 20, text_height + 20])
        win.blit(text, (x, y))

def pause():
    message(win, "PAUSE", white, "large", 0)
    pauseFlag = True
    pygame.display.update()

    while pauseFlag:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pauseFlag = False


def blast(x, y):
    colors = [red, blue, yellow, white, green, inactive_green]
    for i in range(0, 60):
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
        color = int(random.randint(0, 5))
        xpos = int(random.randint(x - 15, x + 15))
        ypos = int(random.randint(y-30, y))
        rad = int(random.randint(2, 30))
        pygame.draw.circle(win, colors[color], (xpos, ypos), rad)
        pygame.display.update()
    
#power should be from 5 to 30
def player_tank_shoot(x, y, turretpos, wallX, wallWidth, wallHeight, enemyX, power = 30):
    global enemyHealth
    shotFlag = True
    t = 0.5
    acc = 2
    theta = radians((1 + turretpos)*7)
    ux = power * cos(theta)
    uy = power * sin(theta)
    while shotFlag:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

        disx = ux * t
        disy = uy * t - 0.5*acc*(t**2)
        xf = round(x - disx)
        yf = round(y - disy)
        t += 0.5
        if yf > groundHeight:
            shotFlag = False
            xcollision = int(x - ux * ((2 * uy / acc) + ((-uy + sqrt((uy ** 2) + 4 * 0.5 * acc * (groundHeight - y))) / acc)))
            if enemyX-10 < xcollision < enemyX+10:
                enemyHealth -= 25
            elif enemyX-20 < xcollision < enemyX+20:
                enemyHealth -= 15
            elif enemyX-30 < xcollision < enemyX+30:
                enemyHealth -= 10
            elif enemyX-40 < xcollision < enemyX+40:
                enemyHealth -= 5
            blast(xcollision, groundHeight)
            break
        elif wallX < xf < wallX + wallWidth and groundHeight - wallHeight < yf < groundHeight:
            shotFlag = False
            blast(xf, yf)
            break
        pygame.draw.circle(win, red, (xf, yf), 3)
        pygame.display.update()

def enemy_tank_shoot(turret_pos, playerX, wallX, wallWidth, wallHeight):
    acc = 2
    min = 900
    powerMin, turretposMin = 1, 1
    global playerHealth
    l, turretpos, power = 0, 0, 1
    for turretpos in range(5, 11):
        if l == 1:
            break
        x1, y1 = turret_pos[turretpos][0], turret_pos[turretpos][1]
        theta = radians((1 + turretpos)*7)
        for i in range(1, 50):
            if l == 1:
                break
            power = i
            t1 = 0.5
            ux1 = power * cos(theta)
            uy1 = power * sin(theta)
            shotFlag1 = True
            while shotFlag1:
                disx1 = ux1 * t1
                disy1 = uy1 * t1 - 0.5 * acc * (t1 ** 2)
                xf1 = round(x1 + disx1)
                yf1 = round(y1 - disy1)
                t1 += 0.5
                if yf1 > groundHeight:
                    shotFlag1 = False
                    xcollision = int(x1 + ux1 * (
                                (2 * uy1 / acc) + ((-uy1 + sqrt((uy1 ** 2) + 4 * 0.5 * acc * (groundHeight - y1))) / acc)))
                    #print(xcollision, playerX, power, "hi")
                    if abs(xcollision - playerX) < min:
                        min = abs(xcollision - playerX)
                        powerMin = power
                        turretposMin = turretpos
                    if playerX - 10 < xcollision < playerX + 10:
                        #print(xcollision, playerX, power)
                        l = 1
                elif wallX < xf1 < wallX + wallWidth and groundHeight - wallHeight < yf1 < groundHeight:
                    shotFlag1 = False
    if l != 1:
        power = powerMin
        turretpos = turretposMin
    power = random.randint(power-1, power+1)

    x, y = turret_pos[turretpos][0], turret_pos[turretpos][1]
    theta = radians((1 + turretpos) * 7)
    ux = power * cos(theta)
    uy = power * sin(theta)
    t = 0.5
    shotFlag = True
    while shotFlag:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

        disx = ux * t
        disy = uy * t - 0.5*acc*(t**2)
        xf = round(x + disx)
        yf = round(y - disy)
        t += 0.5
        if yf > groundHeight:
            shotFlag = False
            xcollision = int(x + ux * ((2 * uy / acc) + ((-uy + sqrt((uy ** 2) + 4 * 0.5 * acc * (groundHeight - y))) / acc)))
            if playerX-10 < xcollision < playerX+10:
                playerHealth -= 20
            elif playerX-20 < xcollision < playerX+20:
                playerHealth -= 15
            elif playerX - 30 < xcollision < playerX + 30:
                playerHealth -= 10
            elif playerX - 40 < xcollision < playerX + 40:
                playerHealth -= 5
            #print(xcollision, playerX, power, "hello")
            blast(xcollision, groundHeight)
            break
        elif wallX < xf < wallX + wallWidth and groundHeight - wallHeight < yf < groundHeight:
            shotFlag = False
            blast(xf, yf)
            break
        pygame.draw.circle(win, red, (xf, yf), 3)
        pygame.display.update()

def tank(x, y, rad, no_of_wheels,wallX, wallWidth, wallHeight, power = 50, turret_pos_index = 3, shot = False, enemy = False, playerXPos = None, enemyX = None):
    pygame.draw.circle(win, red, (x, y), rad)
    pygame.draw.rect(win, red, [x - 2*rad, y, 4*rad, int(2.5*rad)])
    wheels = 4*rad // no_of_wheels
    for i in range(0, no_of_wheels):
        pygame.draw.circle(win, red, ((x - 2*rad) + i*wheels + (wheels // 2), y + int(2.5*rad)), wheels // 2)
    if enemy == False:
        turret_pos = [
                (x - (2*rad + 3), y - 4),
                (x - (2*rad + 2), y - 5),
                (x - (2*rad + 2) + 1, y - 7),
                (x - (2*rad + 2) + 1, y - 8),
                (x - (2*rad + 2) + 1, y - 9),
                (x - (2*rad + 2) + 2, y - 11),
                (x - (2*rad + 2) + 3, y - 13),
                (x - (2*rad + 1) + 4, y - 15),
                (x - (2*rad + 1) + 5, y - 17),
                (x - (2*rad + 1) + 6, y - 19),
                (x - (2*rad) + 6, y - 20)
        ]
    if enemy == True:
        turret_pos = [
            (x + (2 * rad + 3), y - 4),
            (x + (2 * rad + 2), y - 5),
            (x + (2 * rad + 2) + 1, y - 7),
            (x + (2 * rad + 2) + 1, y - 8),
            (x + (2 * rad + 2) + 1, y - 9),
            (x + (2 * rad + 2) + 2, y - 11),
            (x + (2 * rad + 2) + 3, y - 13),
            (x + (2 * rad + 1) + 4, y - 15),
            (x + (2 * rad + 1) + 5, y - 17),
            (x + (2 * rad + 1) + 6, y - 19),
            (x + (2 * rad) + 6, y - 20)
        ]
    pygame.draw.line(win, red, (x, y), (turret_pos[turret_pos_index]), 2)
    if shot == True and enemy == False:
        #power lies between 5 and 30
        player_tank_shoot(turret_pos[turret_pos_index][0], turret_pos[turret_pos_index][1], turret_pos_index, wallX, wallWidth, wallHeight, enemyX, int(5+(30/99)*power))
    elif shot == True and enemy == True:
        enemy_tank_shoot(turret_pos, playerXPos, wallX, wallWidth, wallHeight)

# 1 unit of health bar corresponds to 1 unit of health
# Health bar is of 100 units length
def draw_health_bar(health, x, y, healthBarWidth, healthBarHeight):
    pygame.draw.rect(win, white, [x-1, y-1, healthBarWidth+2, healthBarHeight+2])
    #pygame.draw.rect(win, red, [600, 20, 100, 10])
    pygame.draw.rect(win, red, [x, y, healthBarWidth, healthBarHeight])
    pygame.draw.rect(win, blue, [x, y, health, healthBarHeight])

def Quit():
    pygame.quit()
    quit()

def control():
    controlFlag = True
    while controlFlag:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.fill(black)
        message(win, "CONTROLS", red, "large", -80)
        message(win, "Press up and down arrow keys to rotate the shooter", red, "small", -10)
        message(win, "Press left and right arrow keys to move the tank", red, "small", 20)
        message(win, "Press p to pause", red, "small", 50)
        button("PLAY", green, inactive_green, 100, 500, white, game)
        button("QUIT", green, inactive_green, 600, 500, white, Quit)
        pygame.display.update()

def gameIntro():
    gameIntroFlag = True
    while gameIntroFlag:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.fill(black)
        message(win, "WELCOME", red, "large", -50)
        message(win, "Set power to shoot the enemy tank", red, "small", -20)
        button("PLAY", green, inactive_green, 100, 500, white, game)
        button("CONTROLS", green, inactive_green, 300, 500, white, control)
        button("QUIT", green, inactive_green, 600, 500, white, Quit)

        pygame.display.update()

def gameOver(str):
    gameOverFlag = True
    while gameOverFlag:

        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        message(win, str + " WINS", red, "large", -80)
        button("PLAY AGAIN", green, inactive_green, 100, 400, white, game)
        button("QUIT", green, inactive_green, 600, 400, white, Quit)
        pygame.display.update()

def game():
    gameFlag = True
    count = 0
    turn = 1
    playerTankX = 600
    playerTankY = 500
    tankDomeRadius = 10
    tankWheels = 10
    playerTurretPos = 10
    playerTurretPosChange = 0
    playerTankXChange = 0
    playerHealthBarX = 600
    playerHealthBarY = 20
    power = 50
    powerChange = 0
    global playerHealth
    playerHealth = 100
    healthBarWidth = 100
    healthBarHeight = 10
    global enemyHealth
    enemyHealth = 40
    enemyTankX = 200
    enemyTankXChange = 5
    enemyMove = 40
    enemyTankY = playerTankY
    enemyTurretPos = 10
    enemyHealthBarX = 100
    enemyHealthBarY = 20
    wallX = random.randint(width//2 - int(width*0.2), width//2 + int(width*0.2))
    wallHeight = random.randint(int(groundHeight*0.1), int(groundHeight*0.3))
    wallWidth = 20
    while gameFlag:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_UP:
                    playerTurretPosChange = 1
                elif event.key == pygame.K_DOWN:
                    playerTurretPosChange = -1
                elif event.key == pygame.K_LEFT:
                    playerTankXChange = -3
                elif event.key == pygame.K_RIGHT:
                    playerTankXChange = 3
                elif event.key == pygame.K_d:
                    powerChange = 1
                elif event.key == pygame.K_a:
                    powerChange = -1
                elif event.key == pygame.K_SPACE:
                    tank(playerTankX, playerTankY, tankDomeRadius, tankWheels, wallX, wallWidth, wallHeight, power, playerTurretPos, shot=True, enemy=False, enemyX=enemyTankX)
                    if enemyHealth < 0:
                        gameOver("PLAYER")
                    win.fill(black)
                    win.fill(green, [0, groundHeight, width, width])
                    win.fill(grey, [wallX, groundHeight - wallHeight, wallWidth, wallHeight])
                    message(win, "POWER : " + str(power), white, "small", -height // 2 + 10)
                    tank(playerTankX, playerTankY, tankDomeRadius, tankWheels, wallX, wallWidth, wallHeight, power,
                         playerTurretPos, enemy=False, enemyX=enemyTankX)
                    tank(enemyTankX, enemyTankY, tankDomeRadius, tankWheels, wallX, wallWidth, wallHeight, power,
                         enemyTurretPos, enemy=True)
                    draw_health_bar(playerHealth, playerHealthBarX, playerHealthBarY, healthBarWidth, healthBarHeight)
                    draw_health_bar(enemyHealth, enemyHealthBarX, enemyHealthBarY, healthBarWidth, healthBarHeight)
                    pygame.display.update()

                    tank(enemyTankX, enemyTankY, tankDomeRadius, tankWheels, wallX, wallWidth, wallHeight, turret_pos_index=enemyTurretPos, shot=True, enemy=True, playerXPos=playerTankX)
                    if playerHealth < 0:
                        gameOver("COMPUTER")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerTurretPosChange = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerTankXChange = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    powerChange = 0

        if count == 0:
            if turn == 1:
                enemyTankXChange = 3
            elif turn == 0:
                enemyTankXChange = -3
            count += 1
            turn = (turn + 1) % 2
            move = random.randrange(50, 100)
        elif count == move:
            count = 0
        else:
            count += 1
        #print(count, move, turn, "adsfdasdfads")

        enemyTankX += enemyTankXChange

        playerTurretPos += playerTurretPosChange
        playerTankX += playerTankXChange

        power += powerChange
        
        if playerTurretPos > 10:
            playerTurretPos = 10
        elif playerTurretPos < 0:
            playerTurretPos = 0

        if playerTankX > width:
            playerTankX = width
        elif playerTankX - 2*tankDomeRadius < wallX + wallWidth:
            playerTankX = (wallX + wallWidth) + 2*tankDomeRadius

        if enemyTankX < 0:
            count = 0
            enemyTankX = 0
        elif enemyTankX + 2*tankDomeRadius > wallX:
            count = 0
            enemyTankX = wallX - 2*tankDomeRadius

        if power > 100:
            power = 100
        elif power < 1:
            power = 1
        
        win.fill(black)
        win.fill(green, [0, groundHeight, width, width])
        win.fill(grey, [wallX, groundHeight-wallHeight, wallWidth, wallHeight])
        message(win, "POWER : " + str(power), white, "small", -height // 2 + 10)
        tank(playerTankX, playerTankY, tankDomeRadius, tankWheels, wallX, wallWidth, wallHeight, power, playerTurretPos, enemy = False, enemyX=enemyTankX)
        tank(enemyTankX, enemyTankY, tankDomeRadius, tankWheels, wallX, wallWidth, wallHeight, power, enemyTurretPos, enemy=True)
        draw_health_bar(playerHealth, playerHealthBarX, playerHealthBarY, healthBarWidth, healthBarHeight)
        draw_health_bar(enemyHealth, enemyHealthBarX, enemyHealthBarY, healthBarWidth, healthBarHeight)
        pygame.display.update()

gameIntro()
# wall collision with bullets
# health reduction
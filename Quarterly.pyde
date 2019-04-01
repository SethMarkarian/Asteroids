import random
import math
 
times_asteroid = []
times_fast = []
times_double = []
 
def setup():
    global xRocket, yRocket, angleRocket, xy_coord, xasteroids, yasteroids, xBullet, yBullet, bullet_shot, no_bullet, x_fast_powerup, y_fast_powerup, fast_powerups, fast, anglescale, rocketscale, x_double_powerup, y_double_powerup, double_powerups, double_, fast_powerup, double_powerup, scorescale, score, rocket_hit, lives, endGame, fast_sec, double_sec, asteroid_adding, new_high_score_popup
    size(1320,720)
    background(0)
    xy_coord = []
    for i in range(10):
        asteroidx = random.randrange(width)
        asteroidy = random.randrange(height)
        xy_coord.append([asteroidx, asteroidy, float(random.randrange(0,20))])
    xasteroids = 0
    yasteroids = 0
    xRocket = width/2
    yRocket = height/2
    angleRocket = 0
    bullet_shot = False
    xBullet = width/2
    yBullet = height/2
    keyPressed = True
    no_bullet = True
    fast_powerups = [random.randrange(width), random.randrange(height)]
    fast = False
    anglescale = 3
    rocketscale = 0.05
    double_powerups = [random.randrange(width), random.randrange(height)]
    double_ = False
    fast_powerup = False
    double_powerup = False
    scorescale = 1
    score = 0
    rocket_hit = False
    lives = 1
    endGame = False
    fast_sec = 0
    double_sec = 0
    asteroid_adding = 5
    new_high_score_popup = False
    
def draw():
    global xRocket, yRocket, angleRocket, xy_coord, xasteroids, yasteroids, xBullet, yBullet, bullet_shot, angleBullet, no_bullet, x_fast_powerup, y_fast_powerup, fast_powerups, fast, anglescale, rocketscale, x_double_powerup, y_double_powerup, double_powerups, double_, fast_powerup, double_powerup, scorescale, score, rocket_hit, lives, endGame, fast_sec, double_sec, asteroid_adding, new_high_score_popup
    background(0)
    frameRate(60)
    
    #Asteroids
    pushMatrix()
    translate(xasteroids, yasteroids)
    for i in range(len(xy_coord)):
        stroke(255)
        fill(0)
        if xy_coord[i][0] + xasteroids > width:
            xy_coord[i] = (xy_coord[i][0] - width, xy_coord[i][1])
        if xy_coord[i][1] + yasteroids > height:
            xy_coord[i] = (xy_coord[i][0], xy_coord[i][1] - height)
        stroke(255)
        asteroid(xy_coord[i][0], xy_coord[i][1])
        
    
    xasteroids += 0.5
    yasteroids += 0.5
     
    popMatrix()
 
    #Rocket
    pushMatrix()
    if double_powerup:
        stroke(0,0,255)
    if fast_powerup:
        stroke(255,0,0)
    translate(xRocket, yRocket)
    if xRocket > 1320:
        xRocket = 1319
    if yRocket > 720:
        yRocket = 719
    if xRocket < 1:
        xRocket = 2
    if yRocket < 1:
        yRocket = 2
    pushMatrix()
    rotate(angleRocket)
    rocket()
    popMatrix()
    popMatrix()
    
    #Bullet
    pushMatrix()
    translate(xBullet, yBullet)
    if xBullet > width or yBullet > height or xBullet < 1 or yBullet < 1:
        bullet_shot = False
        no_bullet = True
        xBullet = xRocket
        yBullet = yRocket
    fill(0)
    stroke(0)
    if bullet_shot:
        fill(255)
    bullet()
    popMatrix()
    
    
    #add asteroid
    ms = millis()
    sec = ms // 1000
    if sec % asteroid_adding == 0 and sec != 0 and times_asteroid.count(sec) == 0:
        times_asteroid.append(sec)
        add_circle()
    
    if sec > 20 and sec <= 40:
        asteroid_adding = 4
    if sec > 40 and sec <= 60: 
        asteroid_adding = 3.5
    if sec > 60 and sec <= 80:
        asteroid_adding = 3
    if sec > 80 and sec <=100:
        asteroid_adding = 2.5
    if sec > 100 and sec <= 120:
        asteroid_adding = 2
    if sec > 120 and sec <= 140:
        asteroid_adding = 1.5
    if sec > 140 and sec <= 160:
        asteroid_adding = 1
    if sec > 160:
        asteroid_adding = 0.5
        
    #Remove Asteroid
    # dist(x1,y1,x2,y2) < r1 + r2
    to_remove = -1
    for i in range(len(xy_coord)):
        if dist(xBullet,yBullet,xasteroids + xy_coord[i][0], yasteroids + xy_coord[i][1]) < 27.5 and xBullet != xRocket and yBullet != yRocket:
           to_remove = i
           score += 100 * scorescale
            
    if to_remove != -1:
        xy_coord.pop(to_remove)
        bullet_shot = False
        no_bullet = True
        xBullet = xRocket
        yBullet = yRocket
        
    #If rocket hits asteroid
    #Variable for dying
    rocket_hit = False
    for i in range(len(xy_coord)):
        if dist(xRocket, yRocket, xasteroids + xy_coord[i][0], yasteroids + xy_coord[i][1]) < 45:
            rocket_hit = True
            lives -= 1
            if lives != 0:
                xRocket = width/2
                yRocket = height/2
                xBullet = xRocket
                yBullet = yRocket
            if lives == 0:
                highscore = open("highscore.txt", "r")
                number_highscore = highscore.readline()
                highscore.close()
                if int(number_highscore) < score:
                    highscore = open("highscore.txt", "w")
                    new_highscore = score
                    new_high_score_popup = True
                    highscore.write(str(new_highscore))
                    

                highscore.close()
 
                endGame = True
                fill(255)
                noLoop()
                text("GAME OVER", 550, 300)
                text("FINAL SCORE: " + str(score), 500, 400)
                if new_high_score_popup:
                    text("You got the high score", 500,500)
            
    
 
    
    #Fast Powerup
    pushMatrix()
    if sec % 10 == 0 and sec != 0 and times_fast.count(sec) == 0:
        new_fast()
        fast = True
        
    if fast:
        times_fast.append(sec)
        fill(255,0,0)
        stroke(255,0,0)
        ellipse(fast_powerups[0], fast_powerups[1], 30, 30)
 
    popMatrix()
    if fast:
        fast_powerups[0] -= 0.2
        fast_powerups[1] += 0.2
    
    #Hit Fast
    if fast:
        if dist(xRocket,yRocket, fast_powerups[0], fast_powerups[1]) < 35:
            fast_powerups.pop(-1)
            fast_powerups.pop(-1)
            fast_powerup = True
            double_powerup = False
            fast = False
            fast_sec = millis() + 5000
        if fast_sec < millis():
            fast_powerup = False
        
    if fast_powerup:
        anglescale = 7
        rocketscale = 0.1
    if fast_powerup == False:
        anglescale = 3
        rocketscale = 0.05
        fast_sec = 0
    
    #double points
    pushMatrix()
    if sec % 20 == 0 and sec != 0 and times_double.count(sec) == 0:
        new_double()
        double_ = True
    
    if double_:
        times_double.append(sec)
        fill(0,0,255)
        stroke(0,0,255)
        ellipse(double_powerups[0], double_powerups[1], 30, 30)
 
    popMatrix()
    
    if double_:
        double_powerups[0] += 0.2
        double_powerups[1] -= 0.2
    
    if double_:
        if dist(xRocket,yRocket, double_powerups[0], double_powerups[1]) < 35:
            double_powerups.pop(-1)
            double_powerups.pop(-1)
            double_powerup = True
            fast_powerup = False
            double_ = False
            double_sec = millis() + 5000
        if double_sec < millis():
            double_powerup = False
        
    if double_powerup:
        scorescale = 2
        double_ = False
    
    if double_powerup == False:
        scorescale = 1
    
    #Score
    fill(255)
    textSize(40)
    text("Score:" + str(score), 1000, 40)
    
    highscore = open("highscore.txt", "r")
    number_highscore = highscore.readline()
    textSize(30)
    text("High Score: " + str(number_highscore), 50, 40)
    highscore.close()
    
    
    
    
    #Keyboard inputs
    if keyPressed and key == CODED and keyCode == UP and no_bullet == False:
        yRocket -= anglescale * cos(angleRocket)
        xRocket += anglescale * sin(angleRocket)
    if keyPressed and key == CODED and keyCode == UP and no_bullet:
        yRocket -= anglescale * cos(angleRocket)
        xRocket += anglescale * sin(angleRocket)
        yBullet -= anglescale * cos(angleRocket)
        xBullet += anglescale * sin(angleRocket)
    if keyPressed and key == CODED and keyCode == LEFT:
        angleRocket -= rocketscale
    if keyPressed and key == CODED and keyCode == RIGHT:
        angleRocket += rocketscale
    if keyPressed and key == " " and no_bullet:
        bullet_shot = True
        angleBullet = angleRocket
        
    #If Bullet is in motion
    if bullet_shot:
        yBullet -= 3 * cos(angleBullet)
        xBullet += 3 * sin(angleBullet)
        no_bullet = False
    
#Creates Asteroid centered at point x,y
def asteroid(x, y):
    ellipse(x, y, 50, 50)

#Creates Rocket Shape and rotates it
def rocket():
    rotate(radians(180))
    line(0, 20, 10, -20)
    line(0, 20, -10, -20)
    line(8, -10, -8, -10)
 
#Creates little bullet for the rocket to shoot
def bullet():
    ellipse(0,0,5,5)
 
#Adds an asteroid at a random location
def add_circle():
    global  xy_coord, xasteroids, yasteroids
    x = random.randrange(1200)
    y = random.randrange(720)
    fill(0)
    ellipse(x, y, 50, 50)
    xy_coord.append((x,y))
    
#Adds a new fast powerup on the screen
def new_fast():
    global fast_powerups
    fast_powerups = [random.randrange(width), random.randrange(height)]

#Adds a new double powerup on the screen
def new_double():
    global double_powerups
    double_powerups = [random.randrange(width), random.randrange(height)]
 
 
 

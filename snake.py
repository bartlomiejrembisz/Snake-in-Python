import pygame, sys, random, pickle, pygame.mixer
from time import gmtime, strftime
from pygame.locals import *
from operator import itemgetter
from copy import copy

pygame.init()


#Graphic variables
displayWidth, displayHeight = 800, 600
size = displayWidth, displayHeight
screen = pygame.display.set_caption("Snake by Bartlomiej Rembisz")
screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()

#COLOURS
buttonColour = (0, 191, 255)
COLOURS ={"RED": (255, 0, 0),
          "GREEN": (76, 153, 0),
          "BLUE": (0, 0, 255),
    }

#Fonts
bottomTextFont = pygame.font.SysFont("monospace", 10)
font = pygame.font.SysFont("monospace", 45)
buttonFont = pygame.font.SysFont("monospace", 15)
normalText = pygame.font.SysFont("monospace", 20)
gameoverTextFont = pygame.font.SysFont("monospace", 145)

#Classes
class apple(object):
    """Apple object"""
    
    def __init__(self):
        #Randomising the position of the apple
        self.x = random.randrange(40, 760, 20)
        self.y = random.randrange(40, 560, 20)
        self.pos = [self.x, self.y]
        self.alive = True
        
    #Displaying the apple
    def spawn(self):
        if self.alive == True:
            pygame.draw.rect(screen, (0, 255, 0), ((self.pos), (20, 20)))



class snake(object):
    """Snake object"""
    
    def __init__(self, COLOUR, x, y):
        self.COLOUR = COLOUR
        self.x = x
        self.y = y
        self.length = 0
        self.pos = [[x, y]]

    def display(self):
        snakeHeadFont = pygame.font.SysFont("monospace", 32)
        #Displaying the head
        pygame.draw.rect(screen, self.COLOUR, ((self.pos[0]), (20,20)))

        #Drawing the 'X' on the Snake's head
        text = snakeHeadFont.render("X", 1, (0, 0, 0))
        textrect = text.get_rect()
        textrect.x = self.pos[0][0] + 2
        textrect.y = self.pos[0][1] - 8
        screen.blit(text, textrect)
        
        #Displaying the tail
        for i in range(self.length):
            pygame.draw.rect(screen, snakeColour, ((self.pos[i+1]),(20, 20)))

    
        
def load_hs():
    try:
        scoreFile = open("scores.dat", "rb")
        score = pickle.load(scoreFile)
        scoreFile.close()
    except:
        import traceback
        traceback.print_exc()
        score = [[0, strftime("%H:%M:%S %Y-%m-%d", gmtime())]]
        scoreFile = open("scores.dat", "wb")
        pickle.dump(score, scoreFile)
        scoreFile.close()
    return score


def highscores():
    while True:
        mousePos = pygame.mouse.get_pos()
        screen.fill((255,255,255))
        scoreFile = open("scores.dat", "rb")
        score = pickle.load(scoreFile)
        scoreFile.close()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and (displayWidth/4 - 75 < mousePos[0] < displayWidth/4 - 75 + 150) and (450 < mousePos[1] < 500):
                #Wiping the scores.dat file by overwriting the data with no data.
                scoreFile = open("scores.dat", "wb")
                score = []
                pickle.dump(score, scoreFile)
                scoreFile.close()
            if event.type == MOUSEBUTTONDOWN and (3*displayWidth/4-75 < mousePos[0] < 3*displayWidth/4-75 + 150) and (450 < mousePos[1] < 500):
                menu()
        #Text
        heading = font.render("HIGH SCORES", 1, (0, 0, 0))
        headingrect = heading.get_rect()
        headingrect.x = displayWidth/2-150
        headingrect.y = displayHeight/10
        screen.blit(heading, headingrect)
        
        text = normalText.render("Scores:", 1, (0, 0, 0))
        textrect = text.get_rect()
        textrect.x = 190
        textrect.y = 150
        screen.blit(text, textrect)
        
        text = normalText.render("Date:", 1, (0, 0, 0))
        textrect = text.get_rect()
        textrect.x = displayWidth/2-50
        textrect.y = 150
        screen.blit(text, textrect)
        #Loop that takes out each entry in the array from the .dat file and displays seperately
        y = 180
        for i in score:
            text = normalText.render(str(i[0]), 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = 190
            textrect.y = y
            screen.blit(text, textrect)
            text = normalText.render(str(i[1]), 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = displayWidth/2-50
            textrect.y = y
            screen.blit(text, textrect)
            y+=20          
        #Rectangles
        pygame.draw.rect(screen, buttonColour, ((displayWidth/4-75, 450),(150, 50)))
        pygame.draw.rect(screen, buttonColour, ((3*displayWidth/4-75, 450),(150, 50)))

        #Button text
        if (displayWidth/4 - 75 < mousePos[0] < displayWidth/4 - 75 + 150) and (450 < mousePos[1] < 500):
            text = buttonFont.render("Wipe", 1, (255, 255, 255))
            textrect = text.get_rect()
            textrect.x = displayWidth/4 - 18
            textrect.y = 465
            screen.blit(text, textrect)
        else:
            text = buttonFont.render("Wipe", 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = displayWidth/4 - 18
            textrect.y = 465
            screen.blit(text, textrect)
        if (3*displayWidth/4-75 < mousePos[0] < 3*displayWidth/4-75 + 150) and (450 < mousePos[1] < 500):
            text = buttonFont.render("Menu", 1, (255, 255, 255))
            textrect = text.get_rect()
            textrect.x = 3*displayWidth/4-18
            textrect.y = 465
            screen.blit(text, textrect)
        else:
            text = buttonFont.render("Menu", 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = 3*displayWidth/4-18
            textrect.y = 465
            screen.blit(text, textrect)

        pygame.display.flip()

def game():
    global SCORE, snakeDir
    #Assigning keys in a dictionary to specific sound effects.
    #Sound effects can be found on Freecloud, made by a user called Paul Morek.
    SOUNDS = {1: pygame.mixer.Sound('sound/sound1.wav'),
              2: pygame.mixer.Sound('sound/sound2.wav'),
              3: pygame.mixer.Sound('sound/sound3.wav'),
              4: pygame.mixer.Sound('sound/sound4.wav')
             }
    
    def wall():
        pygame.draw.rect(screen, (0, 0, 0), ((0, 0), (800, 20)))
        pygame.draw.rect(screen, (0, 0, 0), ((0, 0), (20, 600)))
        pygame.draw.rect(screen, (0, 0, 0), ((780, 0), (20, 600)))
        pygame.draw.rect(screen, (0, 0, 0), ((0, 580), (800, 20)))

        
    FPS = 8   
    SCORE = [[0, strftime("%H:%M:%S %Y-%m-%d", gmtime())]]
    player = snake(snakeColour, 400, 300)
    Apple = apple()
    DIRECTIONS = ["RIGHT", "LEFT", "UP", "DOWN"]
    snakeDir = random.choice(DIRECTIONS)
    while True:
        #I use copy() from the copy library to avoid making shared references
        #Then I take the coordinates of the head of the snake and copy it back to the beginning of the array, this way the previous position of the snake is saved
        snake_head = copy(player.pos[0])
        player.pos.insert(0, snake_head)
        #I slice the array to not flood the memory and crash the game.
        player.pos = player.pos[:player.length+1]
        screen.fill((255,255,255))
        clock.tick(FPS)
        movementRestriction = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #Binding keys to directions. I add movement restriction so that in one loop of the game only one move can be done.
                if event.key == K_a and snakeDir != "RIGHT" and movementRestriction == 0:
                    snakeDir = "LEFT"
                    movementRestriction += 1
                if event.key == K_d and snakeDir != "LEFT" and movementRestriction == 0:
                    snakeDir = "RIGHT"
                    movementRestriction += 1
                if event.key == K_w and snakeDir != "DOWN" and movementRestriction == 0:
                    snakeDir = "UP"
                    movementRestriction += 1
                if event.key == K_s and snakeDir != "UP" and movementRestriction == 0:
                    snakeDir = "DOWN"
                    movementRestriction += 1
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        #Player movement. Snake moves 20 pixels each loop
        if snakeDir == "RIGHT":
            player.pos[0][0] += 20
        if snakeDir == "LEFT":
            player.pos[0][0] -= 20
        if snakeDir == "UP":
            player.pos[0][1] -= 20
        if snakeDir == "DOWN":
            player.pos[0][1] += 20
        Apple.spawn()
        player.display()
        if Apple.pos in player.pos[1:]:
            Apple.alive = False
            Apple = apple()
            Apple.spawn()
        #Condition which ends the game if the head of the snake is equal to any of the coordinates in it's tail.
        if player.pos[0] in player.pos[1:]:
            break
        if player.pos[0][0] == Apple.x and player.pos[0][1] == Apple.y:
            if SOUND == 1:
                #The program randomly chooses the sound it plays during the consumption of the apple.
                SOUNDS[random.randint(1, 4)].play()
            Apple.alive = False
            SCORE[0][0] += 10
            player.length += 1
            Apple = apple()
            Apple.spawn()
            if FPS <= 30:
                FPS += 1
        wall()
        #Statement that defines the boundaries of the map, gameover() is ran when the snake crashes into the boundaries
        if (0 <= player.pos[0][0] <= 800 and 0 <= player.pos[0][1] < 20) or (0 <= player.pos[0][0] <= 800 and 580 <= player.pos[0][1] < 600) or (0 <= player.pos[0][0] < 20 and 0 <= player.pos[0][1] <= 600) or (780 < player.pos[0][0] <= 800 and 0 <= player.pos[0][1] <= 600):
            break

        
        #SCORE text
        scoreText = normalText.render("Score:", 1, (255,255,255))
        scoreTextrect = scoreText.get_rect()
        scoreTextrect.x = 650
        scoreTextrect.y = 0
        screen.blit(scoreText, scoreTextrect)
        
        #Display actual SCORE
        scoreText = normalText.render(str(SCORE[0][0]), 1, (255,255,255))
        scoreTextrect = scoreText.get_rect()
        scoreTextrect.x = 725
        scoreTextrect.y = 0
        screen.blit(scoreText, scoreTextrect)

        #Display FPS
        FPStext = normalText.render("FPS: ", 1, (255,255,255))
        FPStextrect = FPStext.get_rect()
        FPStextrect.x = 720
        FPStextrect.y = 580
        screen.blit(FPStext, FPStextrect)
        
        FPStext = normalText.render(str(FPS), 1, (255,255,255))
        FPStextrect = FPStext.get_rect()
        FPStextrect.x = 770
        FPStextrect.y = 580
        screen.blit(FPStext, FPStextrect)


        
        pygame.display.flip()
    gameover()
def gameover():
    r = 0
    score = load_hs()
    score += SCORE
    score.sort(key=lambda playerscore: playerscore[0], reverse = True)
    score = score[:10]
    f = open("scores.dat", "wb")
    pickle.dump(score, f)
    f.close()
    while True:
        #Constant change of colour of the 'Game Over' text
        mousePos = pygame.mouse.get_pos()
        if r == 255:
            add = -5
        elif r == 0:
            add = 5
        r += add
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and (350 < mousePos[0] < 450 and 300 < mousePos[1] < 330):
                game()
            if event.type == MOUSEBUTTONDOWN and (350 < mousePos[0] < 450 and 350 < mousePos[1] < 380):
                highscores()
            if event.type == MOUSEBUTTONDOWN and (350 < mousePos[0] < 450 and 400 < mousePos[1] < 430):
                menu()
                
        pygame.draw.rect(screen, buttonColour, ((displayWidth/2-50, 300),(100,30)))
        pygame.draw.rect(screen, buttonColour, ((displayWidth/2-50, 350),(100,30)))
        pygame.draw.rect(screen, buttonColour, ((displayWidth/2-50, 400),(100,30)))
        
        gameoverText = gameoverTextFont.render("R.I.P", 1, (r, 0, 0))
        gameoverTextrect = gameoverText.get_rect()
        gameoverTextrect.centerx = screen.get_rect().centerx
        gameoverTextrect.centery = displayHeight/4
        screen.blit(gameoverText, gameoverTextrect)

        #SCORE text
        scoreText = normalText.render("Score:", 1, ( 0, 0, 0))
        scoreTextrect = scoreText.get_rect()
        scoreTextrect.centerx = screen.get_rect().centerx
        scoreTextrect.y = (displayHeight/4) + 60
        screen.blit(scoreText, scoreTextrect)
        
        #Display actual SCORE
        scoreText = normalText.render(str(SCORE[0][0]), 1, (0, 0, 0))
        scoreTextrect = scoreText.get_rect()
        scoreTextrect.centerx = screen.get_rect().centerx + 55
        scoreTextrect.y = (displayHeight/4) + 60
        screen.blit(scoreText, scoreTextrect)

        #More text
        scoreText = normalText.render("Your score is being saved in the High Scores section", 1, ( 0, 0, 0))
        scoreTextrect = scoreText.get_rect()
        scoreTextrect.centerx = screen.get_rect().centerx
        scoreTextrect.y = (displayHeight/4) + 80
        screen.blit(scoreText, scoreTextrect)

        #Button text
        if 350 < mousePos[0] < 450 and 300 < mousePos[1] < 330:
            button = buttonFont.render("Restart", 1, (255, 255, 255))
            buttonrect = button.get_rect()
            buttonrect.centerx = screen.get_rect().centerx
            buttonrect.centery = 315
            screen.blit(button, buttonrect)
        else:
            button = buttonFont.render("Restart", 1, (0, 0, 0))
            buttonrect = button.get_rect()
            buttonrect.centerx = screen.get_rect().centerx
            buttonrect.centery = 315
            screen.blit(button, buttonrect)
            
        if 350 < mousePos[0] < 450 and 350 < mousePos[1] < 380:
            button = buttonFont.render("High Scores", 1, (255, 255, 255))
            buttonrect = button.get_rect()
            buttonrect.centerx = screen.get_rect().centerx
            buttonrect.centery = 365
            screen.blit(button, buttonrect)
        else:
            button = buttonFont.render("High Scores", 1, (0, 0, 0))
            buttonrect = button.get_rect()
            buttonrect.centerx = screen.get_rect().centerx
            buttonrect.centery = 365
            screen.blit(button, buttonrect)
            
        if 350 < mousePos[0] < 450 and 400 < mousePos[1] < 430:
            button = buttonFont.render("Menu", 1, (255, 255, 255))
            buttonrect = button.get_rect()
            buttonrect.centerx = screen.get_rect().centerx
            buttonrect.centery = 415
            screen.blit(button, buttonrect)
        else:
            button = buttonFont.render("Menu", 1, (0, 0, 0))
            buttonrect = button.get_rect()
            buttonrect.centerx = screen.get_rect().centerx
            buttonrect.centery = 415
            screen.blit(button, buttonrect)

        
        clock.tick(60)
        pygame.display.flip()

    
def settings():
    global SOUND, snakeColour
    snakeColour = None
    COLOUR = None
    SOUND = 1
    ERROR = 0
    if snakeColour == COLOURS["RED"]:
        COLOUR = "RED"
    if snakeColour == COLOURS["BLUE"]:
        COLOUR = "BLUE"
    if snakeColour == COLOURS["GREEN"]:
        COLOUR = "GREEN"
    while True:
        #Storing the mouse position in a variable mousePos
        mousePos = pygame.mouse.get_pos()
        
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and (50 < mousePos[0] < 200) and (150 < mousePos[1] < 200):
                snakeColour = COLOURS["BLUE"]
                ERROR = 0
            if event.type == MOUSEBUTTONDOWN and (50 < mousePos[0] < 200) and (220 < mousePos[1] < 270):
                snakeColour = COLOURS["RED"]
                ERROR = 0
            if event.type == MOUSEBUTTONDOWN and (50 < mousePos[0] < 200) and (290 < mousePos[1] < 340):
                snakeColour = COLOURS["GREEN"]
                ERROR = 0
            if event.type == MOUSEBUTTONDOWN and (300 < mousePos[0] < 322 and 145 < mousePos[1] < 165):
                SOUND = 1
            if event.type == MOUSEBUTTONDOWN and (345 < mousePos[0] < 380 and 145 < mousePos[1] < 165):
                SOUND = 0
            if event.type == MOUSEBUTTONDOWN and ((displayWidth/2-75) < mousePos[0] < (displayWidth/2+75) and (displayHeight - 100) < mousePos[1] < (displayHeight - 50)) and snakeColour is not None:
                game()
            if event.type == MOUSEBUTTONDOWN and ((displayWidth/2-75) < mousePos[0] < (displayWidth/2+75) and (displayHeight - 100) < mousePos[1] < (displayHeight - 50)) and snakeColour == None:
                ERROR = 1
        #'Settings' text 
        headText = font.render("Settings", 1 , (0,0,0))
        headTextrect = headText.get_rect()
        headTextrect.centerx = screen.get_rect().centerx
        headTextrect.centery = displayHeight/10
        screen.blit(headText, headTextrect)

        #Rectangles
        pygame.draw.rect(screen, buttonColour, ((displayWidth/2 - 150/2,displayHeight - 100),(150, 50)))
        pygame.draw.rect(screen, COLOURS["RED"], ((295, 147),(380 - 295 + 5, 18)))
        if (50 < mousePos[0] < 200) and (150 < mousePos[1] < 200):
            pygame.draw.rect(screen, (0, 191, 255), (50, 150, 150, 50))
        else:
            pygame.draw.rect(screen, (0, 144, 255), (50, 150, 150, 50))
        if (50 < mousePos[0] < 200) and (220 < mousePos[1] < 270):
            pygame.draw.rect(screen, (204, 0, 0), ((50, 220),(150, 50)))
        else:
            pygame.draw.rect(screen, (255, 51, 51), ((50, 220),(150, 50)))
        if (50 < mousePos[0] < 200) and (290 < mousePos[1] < 340):
            pygame.draw.rect(screen, (0, 255, 0), ((50, 290), (150, 50)))
        else:
            pygame.draw.rect(screen, COLOURS["GREEN"], ((50, 290), (150, 50)))

        #Error that occurs when the player doesn't choose the snake's colour
        if ERROR == 1:
            text = buttonFont.render("ERROR: Choose a colour", 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = displayWidth/2 - 100
            textrect.y = displayHeight-125
            screen.blit(text, textrect)
        #Play button text
        if ((displayWidth/2-75) < mousePos[0] < (displayWidth/2+75) and (displayHeight - 100) < mousePos[1] < (displayHeight - 50)):
            text = buttonFont.render("Play", 1, (255, 255, 255))
            textrect = text.get_rect()
            textrect.x = displayWidth/2-(75/4)
            textrect.y = displayHeight-83
            screen.blit(text, textrect)
        else:
            text = buttonFont.render("Play", 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = displayWidth/2-(75/4)
            textrect.y = displayHeight-83
            screen.blit(text, textrect)
        
        #Displays the chosen colour dinamically
        if snakeColour == COLOURS["RED"]:
            COLOUR = "RED"
        if snakeColour == COLOURS["BLUE"]:
            COLOUR = "BLUE"
        if snakeColour == COLOURS["GREEN"]:
            COLOUR = "GREEN"

        CONTROLS = ["CONTROLS:",
                    "W   - UP",
                    "S   - DOWN",
                    "A   - LEFT",
                    "D   - RIGHT",
                    "ESC - EXIT"]
        texty = 130
        for i in CONTROLS:
            text = normalText.render(i, 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = 2*displayWidth/3
            textrect.y = texty
            screen.blit(text, textrect)
            texty += 20
            
        #Text
        colourText = normalText.render("Snake Colour: ", 1, (0,0,0))
        colourTextrect = colourText.get_rect()
        colourTextrect.x = 50
        colourTextrect.y = 125
        screen.blit(colourText, colourTextrect)
        #Displays the chosen colour
        colourText = normalText.render(COLOUR, 1, (0,0,0))
        colourTextrect = colourText.get_rect()
        colourTextrect.x = 210
        colourTextrect.y = 125
        screen.blit(colourText, colourTextrect)
        #'SOUNDS' text
        text = normalText.render("SOUNDS:", 1, (0,0,0))
        textrect = text.get_rect()
        textrect.x = 300
        textrect.y = 125
        screen.blit(text, textrect)
        if SOUND == 1 or (300 < mousePos[0] < 322 and 145 < mousePos[1] < 165):
            text = normalText.render("ON", 1, (0,0,0))
            textrect = text.get_rect()
            textrect.x = 300
            textrect.y = 145
            screen.blit(text, textrect)
        else:
            text = normalText.render("ON", 1, (255,255,255))
            textrect = text.get_rect()
            textrect.x = 300
            textrect.y = 145
            screen.blit(text, textrect)
        rules = ["RULES: ",
                 "Control the snake with the given controls and",
                 "gather the apples", "",
                 "Eating an apple increases the snake's length",
                 "as well as adds 10 to your score",
                 "",
                 "Make sure you don't eat yourself, otherwise",
                 "the game will end",
                 "",
                 "HAVE FUN!!"]
        rulesy = 255
        for i in rules:
            text = normalText.render(i, 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = 240
            textrect.y = rulesy
            screen.blit(text, textrect)
            rulesy += 20
        if SOUND == 0 or (345 < mousePos[0] < 380 and 145 < mousePos[1] < 165):
            text = normalText.render("OFF", 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = 345
            textrect.y = 145
            screen.blit(text, textrect)
        else:
            text = normalText.render("OFF", 1, (255, 255, 255))
            textrect = text.get_rect()
            textrect.x = 345
            textrect.y = 145
            screen.blit(text, textrect)


        pygame.display.flip()
    

def Credits():
    while True:
        #Storing the mouse position in a variable mousePos
        mousePos = pygame.mouse.get_pos()
        
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and (((displayWidth/2-(80/2))+80 > mousePos[0] > (displayWidth/2-(80/2))) and ((500+35) > mousePos[1] > 500)):
                menu()
            
        #'Credits' text in the Credit menu:
        welcomeText = font.render("Credits", 1, (0,0,0))
        welcomeTextrect = welcomeText.get_rect()
        welcomeTextrect.centerx = screen.get_rect().centerx
        welcomeTextrect.centery = displayHeight/10
        screen.blit(welcomeText, welcomeTextrect)

        #Information about the author, me:
        info = ["  Name: Bartlomiej Rembisz",
                "    ID: N0633796",
                "Course: Computer Science",
                "  Year: 1"]
        infoy = 200
        for i in info:
            text = normalText.render(i, 1, (0, 0, 0))
            textrect = text.get_rect()
            textrect.x = 50
            textrect.y = infoy
            screen.blit(text, textrect)
            infoy += 20
            
        #'Back' button
        pygame.draw.rect(screen, buttonColour, (displayWidth/2-(80/2), 500, 80, 35))
        if ((displayWidth/2-(80/2))+80 > mousePos[0] > (displayWidth/2-(80/2))) and ((500+35) > mousePos[1] > 500):
            backButton = buttonFont.render("Back", 1, (255,255,255))
            backButtonrect = backButton.get_rect()
            backButtonrect.centerx = screen.get_rect().centerx
            backButtonrect.y = 508
            screen.blit(backButton, backButtonrect)
        else:
            backButton = buttonFont.render("Back", 1, (0, 0, 0))
            backButtonrect = backButton.get_rect()
            backButtonrect.centerx = screen.get_rect().centerx
            backButtonrect.y = 508
            screen.blit(backButton, backButtonrect)
        
        pygame.display.flip()

        
    
def menu():
    while True:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT: #X button mapped to close the application
                pygame.quit()
                sys.exit()
            #If statement which becomes true if the mouse is placed on the 'Play' rectangle AND the mouse is clicked. 
            elif event.type == MOUSEBUTTONDOWN and (((displayWidth/2-(110/2)+110) > mousePos[0] >(displayWidth/2-(110/2))) and ((textrect.centery+50+50) > mousePos[1] > textrect.centery+50)):
                settings()
            #If statement which becomes true if the mouse is placed on the 'Options' rectangle AND the mouse is clicked.
            elif event.type == MOUSEBUTTONDOWN and (((displayWidth/2-(100/2)+100) > mousePos[0] > ((displayWidth/2-(100/2))) and ((textrect.centery+125+45) > mousePos[1] > textrect.centery+125))):
                highscores()
            #If statement which becomes true if the mouse is placed on the 'Credits' rectangle AND the mouse is clicked.
            elif event.type == MOUSEBUTTONDOWN and ((((displayWidth/2-(90/2))+90) > mousePos[0] > (displayWidth/2-(90/2))) and ((textrect.centery+200+40) > mousePos[1] > textrect.centery+200)):
                Credits()
            #If statement which becomes true if the mouse is placed on the 'Quit' rectangle AND the mouse is clicked.
            elif event.type == MOUSEBUTTONDOWN and (((displayWidth/2-(80/2))+80 > mousePos[0] > (displayWidth/2-(80/2))) and ((textrect.centery+275+35) > mousePos[1] > textrect.centery+275)):
                pygame.quit()
                sys.exit()
                
        #'Welcome to Snake by pyGame' text in menu
        text = font.render("Welcome to Snake in pyGame!", 1, (0,0,0))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = displayHeight/10
        screen.blit(text, textrect)
        bottomText = bottomTextFont.render("(c) Bartlomiej Rembisz", 1, (0,0,0))
        bottomTextrect = bottomText.get_rect()
        bottomTextrect.centerx = screen.get_rect().centerx
        bottomTextrect.centery = 550
        screen.blit(bottomText, bottomTextrect)

        #Storing the mouse position in a variable mousePos
        mousePos = pygame.mouse.get_pos()
        
        #Rectangles in menu
        pygame.draw.rect(screen, buttonColour, (displayWidth/2-(110/2), textrect.centery+50, 110, 50))
        pygame.draw.rect(screen, buttonColour, (displayWidth/2-(100/2), textrect.centery+125, 100, 45))
        pygame.draw.rect(screen, buttonColour, (displayWidth/2-(90/2), textrect.centery+200, 90, 40))
        pygame.draw.rect(screen, buttonColour, (displayWidth/2-(80/2), textrect.centery+275, 80, 35))



        
        #Button labels set up so that the font changes colour as the user swipes over the rectangles holding the text.
        #Button no.1, 'Play'
        #Mouse over the rectangle:
        if ((displayWidth/2-(110/2)+110) > mousePos[0] >(displayWidth/2-(110/2))) and ((textrect.centery+50+50) > mousePos[1] > textrect.centery+50):
            button1 = buttonFont.render("Play!", 1, (255,255,255))
            buttonrect1 = button1.get_rect()
            buttonrect1.centerx = screen.get_rect().centerx
            buttonrect1.centery = textrect.centery+75
            screen.blit(button1, buttonrect1)
        #Mouse not over the rectangle:
        else:
            button1 = buttonFont.render("Play!", 1, (0,0,0))
            buttonrect1 = button1.get_rect()
            buttonrect1.centerx = screen.get_rect().centerx
            buttonrect1.centery = textrect.centery+75
            screen.blit(button1, buttonrect1)
            
        #Button no. 2, 'Options'
        #Mouse over the rectangle:
        if (((displayWidth/2-(100/2)+100) > mousePos[0] > ((displayWidth/2-(100/2))) and ((textrect.centery+125+45) > mousePos[1] > textrect.centery+125))):
            button1 = buttonFont.render("High Scores", 1, (255,255,255))
            buttonrect1 = button1.get_rect()
            buttonrect1.centerx = screen.get_rect().centerx
            buttonrect1.centery = textrect.centery+147
            screen.blit(button1, buttonrect1)
        #Mouse not over the rectangle:
        else:
            button1 = buttonFont.render("High Scores", 1, (0,0,0))
            buttonrect1 = button1.get_rect()
            buttonrect1.centerx = screen.get_rect().centerx
            buttonrect1.centery = textrect.centery+147
            screen.blit(button1, buttonrect1)
            
        #Button no.2, 'Credits'
        #Mouse over the rectangle:
        if (((displayWidth/2-(90/2))+90) > mousePos[0] > (displayWidth/2-(90/2))) and ((textrect.centery+200+40) > mousePos[1] > textrect.centery+200):
            button1 = buttonFont.render("Credits", 1, (255,255,255))
            buttonrect1 = button1.get_rect()
            buttonrect1.centerx = screen.get_rect().centerx
            buttonrect1.centery = textrect.centery+220
            screen.blit(button1, buttonrect1)
        #Mouse not over the rectangle:
        else:
            button1 = buttonFont.render("Credits", 1, (0,0,0))
            buttonrect1 = button1.get_rect()
            buttonrect1.centerx = screen.get_rect().centerx
            buttonrect1.centery = textrect.centery+220
            screen.blit(button1, buttonrect1)
            
        #Button no.3, 'Quit'
        #Mouse over the rectangle:
        if ((displayWidth/2-(80/2))+80 > mousePos[0] > (displayWidth/2-(80/2))) and ((textrect.centery+275+35) > mousePos[1] > textrect.centery+275):
            button1 = buttonFont.render("Quit", 1, (255,255,255))
            buttonrect1 = button1.get_rect()
            buttonrect1.centerx = screen.get_rect().centerx
            buttonrect1.centery = textrect.centery+292
            screen.blit(button1, buttonrect1)
        #Mouse not over the rectangle:
        else:
            button1 = buttonFont.render("Quit", 1, (0,0,0))
            buttonrect1 = button1.get_rect()
            buttonrect1.centerx = screen.get_rect().centerx
            buttonrect1.centery = textrect.centery+292
            screen.blit(button1, buttonrect1)
        
        clock.tick(60) 
        pygame.display.flip()

def main():
    menu()
main()

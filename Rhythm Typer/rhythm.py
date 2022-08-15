import pygame, sys, string, random
from pygame.locals import *

pygame.init()

# Initializes the two fonts the game uses
font = pygame.font.SysFont("Times New Roman", 18)
Font = pygame.font.SysFont("Arial", 80)
Font.set_bold(True)

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (222, 222, 0)
PURPLE = (255, 0, 255)
ORANGE = (222, 120, 0)
PINK = (255, 190, 200)
BROWN = (140, 70, 20)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)
WHITE = (255, 255, 255)

# Initializes combo, score, and lives
combo = 0
score = 0
lives = 3
comboLabel = Font.render(str(combo) + "x", 1, WHITE)
scoreLabel = Font.render("Score: " + str(score), 1, WHITE)
livesLabel = Font.render("Lives: " + str(lives), 1, WHITE)
note_list = []
note_n = -1

# Initializes window
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
screen.fill(BLACK)
pygame.display.set_caption("Rhythm Game")
FPS = 30
FramePerSec = pygame.time.Clock()
running = True

# Plays music
volume = 0.6
volumeLabel = font.render("Volume: " + str(volume), 1, WHITE)
pygame.mixer.music.load('Mid-Summer_Dream.mp3')
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

# Spawn timer of letters
BPM = 120
SPAWNEVENT, t, trail = pygame.USEREVENT+1, (BPM / 60) * 1000, []
pygame.time.set_timer(SPAWNEVENT, int(t))
DoubleTime = False
TripleTime = False

# Defines note class
class Note(pygame.sprite.Sprite):
    def __init__(self, nletter):
        self.nletter = nletter
        pygame.sprite.Sprite.__init__(self)
        self.image = Font.render(nletter, 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 0)

    def fall(self):
        if self.rect.y > HEIGHT:
            global note_n
            global note_list
            global combo
            global score
            global comboLabel
            global scoreLabel
            global livesLabel
            global lives
            global DoubleTime
            global TripleTime
            del note_list[note_n]
            note_n -= 1
            score -= combo
            combo = 0
            lives -= 1
            livesLabel = Font.render("Lives: " + str(lives), 1, WHITE)
            comboLabel = Font.render(str(combo) + "x", 1, WHITE)
            scoreLabel = Font.render("Score: " + str(score), 1, WHITE)
            if DoubleTime == True or TripleTime == True:
                BPM = 120
                SPAWNEVENT, t, trail = pygame.USEREVENT+1, (BPM / 60) * 1000, []
                pygame.time.set_timer(SPAWNEVENT, int(t))
                DoubleTime = False
                TripleTime = False
        else:
            self.rect.y += 25

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Defines player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([WIDTH, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT * 0.75)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def hit(self, Note, letter):
        global note_n
        global note_list
        global combo
        global score
        global comboLabel
        global scoreLabel
        global livesLabel
        global lives
        global DoubleTime
        global TripleTime
        if pygame.sprite.collide_rect(self, Note) and letter.upper() == Note.nletter:
            combo += 1
            score += combo * lives
            comboLabel = Font.render(str(combo) + "x", 1, WHITE)
            scoreLabel = Font.render("Score: " + str(score), 1, WHITE)
            del note_list[note_n]
            note_n -= 1
            if combo >= 10 and DoubleTime == False:
                BPM = 90
                SPAWNEVENT, t, trail = pygame.USEREVENT+1, (BPM / 60) * 1000, []
                pygame.time.set_timer(SPAWNEVENT, int(t))
                DoubleTime = True
            if combo >= 20 and TripleTime == False:
                BPM = 60
                SPAWNEVENT, t, trail = pygame.USEREVENT+1, (BPM / 60) * 1000, []
                pygame.time.set_timer(SPAWNEVENT, int(t))
                TripleTime = True
        else:
            del note_list[note_n]
            note_n -= 1
            score -= combo
            combo = 0
            lives -= 1
            comboLabel = Font.render(str(combo) + "x", 1, WHITE)
            scoreLabel = Font.render("Score: " + str(score), 1, WHITE)
            livesLabel = Font.render("Lives: " + str(lives), 1, WHITE)
            if DoubleTime == True or TripleTime == True:
                BPM = 120
                SPAWNEVENT, t, trail = pygame.USEREVENT+1, (BPM / 60) * 1000, []
                pygame.time.set_timer(SPAWNEVENT, int(t))
                DoubleTime = False
                TripleTime = False

# Defines what happens when the game ends
def GameOver():
    global running
    running = False
    pygame.mixer.music.stop()
    screen.fill(BLACK)
    GameOverLabel = Font.render("Game Over!", 1, WHITE)
    InputInitialLabel = font.render("Input a letter and then check highscores.txt to see your score", 1, WHITE)
    TipLabel = font.render("Tip: Check tutorial.txt for controls and instructions", 1, WHITE)
    screen.blit(GameOverLabel, ((WIDTH / 2) - 200, (HEIGHT / 2) - 200))
    screen.blit(InputInitialLabel, ((WIDTH / 2) - 200, (HEIGHT / 2)))
    screen.blit(TipLabel, ((WIDTH / 2) - 175, (HEIGHT / 2) + 75))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                with open('highscores.txt', 'a') as text_file:
                    text_file.write(f"{score} {chr(event.key)}\n")
                pygame.quit()
                sys.exit()

Player = Player()

# Game Loop
while running == True:
    if score < 50:
        screen.fill(BLACK)
    elif score < 100:
        screen.fill(PURPLE)
    elif score < 250:
        screen.fill(BLUE)
    elif score < 500:
        screen.fill(GREEN)
    elif score < 750:
        screen.fill(YELLOW)
    elif score < 1000:
        screen.fill(ORANGE)
    else:
        screen.fill(RED)
    # Handles game over
    if lives < 1:
        GameOver()
    for event in pygame.event.get():
        # Quits the game with X button
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Quits the game with ESC key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Manages volume with +/-
            if event.key == pygame.K_EQUALS:
                volume += 0.05
                pygame.mixer.music.set_volume(volume)
                volumeLabel = font.render("Volume: " + str(round((volume), 2)), 1, WHITE)
            if event.key == pygame.K_MINUS:
                volume -= 0.05
                pygame.mixer.music.set_volume(volume)
                volumeLabel = font.render("Volume: " + str(round((volume), 2)), 1, WHITE)
            # Registers key taps
            if event.key == pygame.K_a:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "a")
            if event.key == pygame.K_b:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "b")
            if event.key == pygame.K_c:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "c")
            if event.key == pygame.K_d:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "d")
            if event.key == pygame.K_e:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "e")
            if event.key == pygame.K_f:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "f")
            if event.key == pygame.K_g:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "g")
            if event.key == pygame.K_h:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "h")
            if event.key == pygame.K_i:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "i")
            if event.key == pygame.K_j:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "j")
            if event.key == pygame.K_k:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "k")
            if event.key == pygame.K_l:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "l")
            if event.key == pygame.K_m:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "m")
            if event.key == pygame.K_n:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "n")
            if event.key == pygame.K_o:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "o")
            if event.key == pygame.K_p:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "p")
            if event.key == pygame.K_q:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "q")
            if event.key == pygame.K_r:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "r")
            if event.key == pygame.K_s:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "s")
            if event.key == pygame.K_t:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "t")
            if event.key == pygame.K_u:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "u")
            if event.key == pygame.K_v:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "v")
            if event.key == pygame.K_w:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "w")
            if event.key == pygame.K_x:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "x")
            if event.key == pygame.K_y:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "y")
            if event.key == pygame.K_z:
                if len(note_list) > 0:
                    Player.hit(note_list[note_n], "z")
        # Manages volume with scroll wheel
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:   
                volume += 0.05
                pygame.mixer.music.set_volume(volume)
                volumeLabel = font.render("Volume: " + str(round((volume), 2)), 1, WHITE)
            if event.button == 5:   
                volume -= 0.05
                pygame.mixer.music.set_volume(volume)
                volumeLabel = font.render("Volume: " + str(round((volume), 2)), 1, WHITE)
        # Allows resizing of window
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            WIDTH = event.w
            HEIGHT = event.h
        if event.type == SPAWNEVENT:
            new_note = Note(random.choice(string.ascii_uppercase))
            note_list.append(new_note)
            note_n += 1
    screen.blit(volumeLabel, (WIDTH - 100, 0))
    screen.blit(comboLabel, ((WIDTH / 2) - 50, HEIGHT - 100))
    screen.blit(scoreLabel, (0, 0))
    screen.blit(livesLabel, (0, 100))
    for note in note_list:
        note.draw(screen)
        note.fall()
        comboLabel = Font.render(str(combo) + "x", 1, WHITE)
    Player.draw(screen)
    pygame.display.update()
    FramePerSec.tick(FPS)
    

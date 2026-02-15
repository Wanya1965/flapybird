from pygame import*
from random import randint
import sounddevice as sd
import numpy as np
from time import sleep

sr = 16000
block = 256
mic_level = 0.0

def audio_cb(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

init()
window_size = 800 , 600
window = display.set_mode(window_size)
clock = time.Clock()

player_rect = Rect(50,500 , 100 , 100)

def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
    pipes = []
    start_x = 1200
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        bottom_pipe = Rect(start_x, height + gap, pipe_width, 800- (height + gap))
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

pies = generate_pipes(150)
main_font = font.Font(None, 100)
score = 0 
lose = False
y_vel = 2
wait = 40
win=False
gravity = 0.6
THRESH = 0.001
IMPULSE = -8.0

with sd.InputStream(samplerate=sr, channels=1, blocksize=block, callback=audio_cb):

    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()
        window.fill((0,0,255))
        draw.rect(window, 'red', player_rect)
        for pie in pies:
            if not lose:
                pie.x -= 10
            draw.rect(window, 'green', pie)
            if pie.x <= -100:
                pies.remove(pie)
                score+=0.5
            if player_rect.colliderect(pie):
                lose = True
        if len(pies) < 8:
            pies += generate_pipes(150)
        keys = key.get_pressed()
        if keys[K_w] and not lose:
            player_rect.y -=15
        if keys[K_s] and not lose:
            player_rect.y +=15


        if mic_level > THRESH:
            y_vel = IMPULSE
        y_vel += gravity
        player_rect.y += int(y_vel)


        score_text = main_font.render(f'{int(score)}', 1, 'black')
        window.blit(score_text,(600,40))
        

        if keys[K_r] and lose:
            win=False
            lose=False 
            score = 0
            pies = generate_pipes(150)
            player_rect.y = 300
            y_vel = 2
        if player_rect.bottom > 800:
            player_rect.bottom = 800
            y_vel = 0.0
        if player_rect.top <0:
            player_rect.top = 0
            if y_vel <0:
                y_vel = 0.0

        display.update()
        clock.tick(60)

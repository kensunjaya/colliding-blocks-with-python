import pygame as game
from win32api import GetSystemMetrics

screen_size = (GetSystemMetrics(0), GetSystemMetrics(1))

game.init()
game.font.init()

font = game.font.Font(None, 48)
desc_font = game.font.Font(None, 28)

screen = game.display.set_mode(screen_size)
tick_sound = game.mixer.Sound("tick.wav")
screen.set_alpha(None)
clock = game.time.Clock()
running = True
dt = 0
collision = 0
distance = 0
white = (255, 255, 255)
infinite_collision = True


class B1:  # larger object
    m = 100
    v1 = -300
    v2 = 0
    size = 200
    x = screen_size[0] * 0.65
    y = screen_size[1] * 0.5


class B2:  # smaller object
    m = 1
    v1 = 0
    v2 = 0
    size = 100
    x = screen_size[0] * 0.4
    y = screen_size[1] * 0.5 + (B1.size - size)


while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    distance = B1.x - (B2.x + B2.size)
    screen.fill("black")
    text_surface = font.render("Collision : " + str("{:,}".format(collision)), True, white)
    b1_mass = desc_font.render(str("{:,}".format(B1.m)) + " kg", True, white)
    b1_velocity = desc_font.render(str(round(B1.v1, 10)) + " px/s", True, white)
    b2_mass = desc_font.render(str("{:,}".format(B2.m)) + " kg", True, white)
    b2_velocity = desc_font.render(str(round(B2.v1, 10)) + " px/s", True, white)
    distance_text = font.render("Distance : " + str("{:,}".format(int(distance))), True, white)
    screen.blit(text_surface, dest=(50, 50))
    screen.blit(distance_text, dest=(50, 100))
    screen.blit(b1_mass, dest=(B1.x, B1.y - 50))
    screen.blit(b2_mass, dest=(B2.x, B2.y - 50))
    screen.blit(b1_velocity, dest=(B1.x, B1.y - 25))
    screen.blit(b2_velocity, dest=(B2.x, B2.y - 25))
    box1 = game.draw.rect(screen, white, game.Rect(B1.x, B1.y, B1.size, B1.size))
    box2 = game.draw.rect(screen, white, game.Rect(B2.x, B2.y, B2.size, B2.size))
    track = game.draw.line(screen, (0, 255, 0), (0, B1.y + B1.size), (screen_size[0], B1.y + B1.size), 5)

    while (B2.v1 > 20000) or (B2.v1 < -20000): # Calculate the momentum without updating the screen to speed up process
        if ((B2.x + B2.size) >= B1.x) and (B1.v1 <= B2.v1):  # if collision occur
            collision += 1

            B1.v2 = (((B1.m * B1.v1) + (B2.m * B2.v1)) - (B2.m * (B1.v1 - B2.v1))) / (B1.m + B2.m)
            B2.v2 = B1.v2 + (B1.v1 - B2.v1)

            B1.v1 = B1.v2
            B2.v1 = B2.v2

        elif (B2.x <= 0) and (B2.v1 < 0):
            collision += 1
            B2.v1 *= -1
        elif (B1.x + B1.size >= screen_size[0]) and (B1.v1 > 0):
            if infinite_collision:
                collision += 1
                B1.v1 *= -1

        B1.x += B1.v1 * dt
        B2.x += B2.v1 * dt

    if ((B2.x + B2.size) >= B1.x) and (B1.v1 <= B2.v1):  # if collision occur
        collision += 1
        game.mixer.Sound.play(tick_sound)

        B1.v2 = (((B1.m * B1.v1) + (B2.m * B2.v1)) - (B2.m * (B1.v1 - B2.v1))) / (B1.m + B2.m)
        B2.v2 = B1.v2 + (B1.v1 - B2.v1)

        B1.v1 = B1.v2
        B2.v1 = B2.v2

    elif (B2.x <= 0) and (B2.v1 < 0):
        collision += 1
        game.mixer.Sound.play(tick_sound)
        B2.v1 *= -1
    elif (B1.x + B1.size >= screen_size[0]) and (B1.v1 > 0):
        if infinite_collision:
            collision += 1
            game.mixer.Sound.play(tick_sound)
            B1.v1 *= -1

    B1.x += B1.v1 * dt
    B2.x += B2.v1 * dt

    game.display.flip()
    dt = clock.tick(100000000) / 1000

game.quit()

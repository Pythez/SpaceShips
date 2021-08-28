import pygame
import os #helps define path to images
pygame.font.init() #enable font library for text (player hp)
pygame.mixer.init() #enables sound for pygame
#top left coordinate = 0,0

white, black = (255, 255, 255), (0, 0, 0)

width, height = 900, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("SpaceShips")

velocity, bullet_velocity = 3, 7
fps = 144
max_bullets = 3
spaceship_width, spaceship_height = 55, 40
yellow_hit, red_hit = pygame.USEREVENT + 1, pygame.USEREVENT + 2

border = pygame.Rect(width//2 - 5, 0, 10, height) #x, y, width, height

health_font, winner_font = pygame.font.SysFont('comicsans', 45), pygame.font.SysFont('comicsans', 100)

#IMPORTED ASSETS
victory_sound = pygame.mixer.Sound(os.path.join('PyGame', 'Assets', 'victory.wav'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('PyGame', 'Assets', 'gunshot.wav'))

yellow_ship_unsized = pygame.image.load(os.path.join('PyGame', 'Assets', 'spaceship_yellow.png'))
yellow_ship = pygame.transform.rotate(pygame.transform.scale(yellow_ship_unsized, (spaceship_width, spaceship_height)), 90)

space = pygame.transform.scale(pygame.image.load(os.path.join('PyGame', 'Assets', 'space.png')),(width, height))

red_ship_unsized = pygame.image.load(os.path.join('PyGame', 'Assets', 'spaceship_red.png'))
red_ship = pygame.transform.rotate(pygame.transform.scale(red_ship_unsized, (spaceship_width, spaceship_height)), 270)

def draw_window(red,yellow,black,yellow_bullets,red_bullets,red_health,yellow_health):
    window.blit(space,(0,0)) #red green blue RGB 0 - 255
    pygame.draw.rect(window, black, border)
    red_health_text = health_font.render("Health: " + str(red_health), 1, white)
    yellow_health_text = health_font.render("Health: " + str(yellow_health), 1, white)
    window.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    window.blit(yellow_health_text, (10, 10))
    window.blit(yellow_ship, (yellow.x, yellow.y)) #blit to draw surface on the screen
    window.blit(red_ship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(window, (255, 0, 0), bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(window, black, bullet)
        
    pygame.display.update()

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_velocity
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet) #we need event to edit the bullet lists in the main loop
        elif bullet.x > width:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_velocity
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - velocity > 0 : #LEFT
        yellow.x -= velocity
    if keys_pressed[pygame.K_d] and yellow.x + velocity + yellow.width < border.x : #RIGHT
        yellow.x += velocity
    if keys_pressed[pygame.K_w] and yellow.y - velocity > 0: #UP
        yellow.y -= velocity
    if keys_pressed[pygame.K_s] and yellow.y + velocity + yellow.height < height - 15 : #DOWN with hardcoded value
        yellow.y += velocity

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - velocity > border.x + border.width: #LEFT
        red.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + velocity + red.width < width: #RIGHT
        red.x += velocity
    if keys_pressed[pygame.K_UP] and red.y - velocity > 0: #UP
        red.y -= velocity
    if keys_pressed[pygame.K_DOWN] and red.y + velocity + red.height < height - 15: #DOWN
        red.y += velocity
    
def draw_winner(text):
    draw_text = winner_font.render(text, 1, white)
    window.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    victory_sound.play()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)

    red_bullets, yellow_bullets = [], []
    red_health, yellow_health = 10, 10
    winner_text = ''
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(fps)
        for event in pygame.event.get(): # looping through list of all events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) #minus 2 because bullet height is 5
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2, 10, 5) #minus 2 because bullet height is 5
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 1
            if event.type == yellow_hit:
                yellow_health -= 1

        if red_health <= 0:
            winner_text = 'Yellow Wins!'  
        if yellow_health <= 0:
            winner_text = 'RED Wins!'       
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)   
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, black,  yellow_bullets, red_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__": #only starts main when we execute file
    main()

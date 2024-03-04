import pygame
import random
import sys

# Konstanten für das Spiel
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
SCORE_COLOR = (0, 0, 0)
PLAYER_SIZE = 60
OBSTACLE_WIDTH = 120
OBSTACLE_HEIGHT = 90
PLAYER_SPEED = 5
OBSTACLE_SPEED = 3
OBSTACLE_SPAWN_INTERVAL = 60  # Hindernisse erscheinen alle 60 Frames (1 Sekunde)
JUMP_HEIGHT = 100
JUMP_DURATION = 20  # Dauer des Sprungs in Frames

# Initialisierung von Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cross the Road")
clock = pygame.time.Clock()

# Laden der Bilder
frog_png = pygame.image.load("frog.png").convert_alpha()
car_png = pygame.image.load("car.png").convert_alpha()
street_jpg = pygame.image.load("street.jpg").convert()

# Anpassung der Bildgröße
frog_png = pygame.transform.scale(frog_png, (PLAYER_SIZE, PLAYER_SIZE))
car_png = pygame.transform.scale(car_png, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
street_jpg = pygame.transform.scale(street_jpg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Spielerklasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = frog_png
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.is_jumping = False
        self.jump_count = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED

        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.is_jumping = True
            self.jump_count = JUMP_DURATION

        if self.is_jumping:
            if self.jump_count >= -JUMP_DURATION:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.05 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False

# Hindernisklasse
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = car_png
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.reset()
        elif self.speed < 0 and self.rect.right < 0:
            self.reset()

    def reset(self):
        self.rect.y = random.randint(60, SCREEN_HEIGHT - self.rect.height - 60)  
        self.rect.right = SCREEN_WIDTH  
        self.speed = -OBSTACLE_SPEED  

# Funktion zur Anzeige des Punktestands
def display_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, SCORE_COLOR)
    screen.blit(text, (10, 10))

# Hauptspiel-Funktion
def main():
    player = Player()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    score = 0
    paused = False

    obstacle_spawn_counter = 0  # Zähler für das Erscheinen von Hindernissen

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            # Hindernisse hinzufügen
            obstacle_spawn_counter += 1
            if obstacle_spawn_counter >= OBSTACLE_SPAWN_INTERVAL:
                speed = random.choice([-OBSTACLE_SPEED, OBSTACLE_SPEED])
                obstacle = Obstacle(speed)
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
                obstacle_spawn_counter = 0

            # Kollisionserkennung
            collisions = pygame.sprite.spritecollide(player, obstacles, False)
            if collisions:
                running = False

            # Spieler-Update
            player.update()

            # Hindernis-Update
            obstacles.update()

            # Hintergrund zeichnen
            screen.blit(street_jpg, (0, 0))

            # Alle Sprites zeichnen
            all_sprites.draw(screen)

            # Punktestand anzeigen
            display_score(score)

            # Spiel aktualisieren
            pygame.display.flip()

            # Frames pro Sekunde festlegen
            clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 

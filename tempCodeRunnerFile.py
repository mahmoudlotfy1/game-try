import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
w, h = 800, 600
Screengame = pygame.display.set_mode((w, h))
pygame.display.set_caption('Monster Shooting Game')
FPS = 60

# Load animations
walk_right = [pygame.image.load(f"walkright{i}.png") for i in range(1, 8)]
walk_up = [pygame.image.load(f"walk_up{i}.png") for i in range(1, 8)]
stand = [pygame.image.load(f"idle_down{i}.png") for i in range(1, 9)]

# Player class
class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_numbers = 0
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.stop = True

    def draw(self, display):
        if self.animation_numbers + 1 > 49:
            self.animation_numbers = 0
        self.animation_numbers += 1
        if self.right:
            display.blit(pygame.transform.scale(walk_right[self.animation_numbers // 8], (self.width, self.height)), (self.x, self.y))
        elif self.left:
            display.blit(pygame.transform.scale(pygame.transform.flip(walk_right[self.animation_numbers // 8], True, False), (self.width, self.height)), (self.x, self.y))
        elif self.up:
            display.blit(pygame.transform.scale(walk_up[self.animation_numbers // 8], (self.width, self.height)), (self.x, self.y))
        elif self.down:
            display.blit(pygame.transform.scale(pygame.transform.flip(walk_up[self.animation_numbers // 8], False, True), (self.width, self.height)), (self.x, self.y))
        elif self.stop:
            display.blit(pygame.transform.scale(stand[self.animation_numbers // 9], (self.width, self.height)), (self.x, self.y))

        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.stop = True

# Bullet class for player and monster
class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 15
        self.angle = math.atan2(target_y - y, target_x - x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self, display):
        pygame.draw.circle(display, (255, 0, 0), (int(self.x), int(self.y)), 5)

# Monster class
class Monster:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.last_shot = 0

    def draw(self, display):
        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 5:  # Move only if the player is farther than 5 pixels
            direction_x = dx / distance
            direction_y = dy / distance
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed

    def shoot(self, player, current_time, monster_bullets):
        if current_time - self.last_shot > 1000:  # Shoot every 1 second
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, player.x, player.y)
            monster_bullets.append(bullet)
            self.last_shot = current_time

# Initialize game objects
the_player = Player(400, 300, 40, 50)
monster = Monster(0, 0, 40, 50, speed=2)
player_bullets = []
monster_bullets = []

shooting = False

def Game():
    global shooting
    fps = pygame.time.Clock()
    run = True

    while run:
        Screengame.fill((50, 150, 100))
        fps.tick(FPS)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not shooting:
                    bullet = Bullet(the_player.x + the_player.width // 2, the_player.y + the_player.height // 2, mouse_x, mouse_y)
                    player_bullets.append(bullet)
                    shooting = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    shooting = False

        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            the_player.x -= 5
            the_player.left = True
            the_player.stop = False
        if keys[pygame.K_d]:
            the_player.x += 5
            the_player.right = True
            the_player.stop = False
        if keys[pygame.K_w]:
            the_player.y -= 5
            the_player.up = True
            the_player.stop = False
        if keys[pygame.K_s]:
            the_player.y += 5
            the_player.down = True
            the_player.stop = False

        # Draw and update player
        the_player.draw(Screengame)

        # Monster actions
        monster.move_towards_player(the_player)
        monster.draw(Screengame)
        monster.shoot(the_player, current_time, monster_bullets)

        # Update and draw bullets
        for bullet in player_bullets[:]:
            bullet.update()
            bullet.draw(Screengame)
            if bullet.x < 0 or bullet.x > w or bullet.y < 0 or bullet.y > h:
                player_bullets.remove(bullet)

        for bullet in monster_bullets[:]:
            bullet.update()
            bullet.draw(Screengame)
            if bullet.x < 0 or bullet.x > w or bullet.y < 0 or bullet.y > h:
                monster_bullets.remove(bullet)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    Game()

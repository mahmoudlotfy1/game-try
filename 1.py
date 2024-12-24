import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

w = 1000
h = 700
Screengame = pygame.display.set_mode((w, h))
pygame.display.set_caption('Boss Fight')
FPS = 60

bg= pygame.image.load("ground.png")

# The image of movement animation
walk_right = [pygame.image.load("walkright1.png"), pygame.image.load("walkright2.png"),
              pygame.image.load("walkright3.png"), pygame.image.load("walkright4.png"),
              pygame.image.load("walkright5.png"), pygame.image.load("walkright6.png"),
              pygame.image.load("walkright7.png")]

walk_up = [pygame.image.load("walk_up1.png"), pygame.image.load("walk_up2.png"),
           pygame.image.load("walk_up3.png"), pygame.image.load("walk_up4.png"),
           pygame.image.load("walk_up5.png"), pygame.image.load("walk_up6.png"),
           pygame.image.load("walk_up7.png")]

stand = [pygame.image.load("idle_down1.png"), pygame.image.load("idle_down2.png"),
         pygame.image.load("idle_down3.png"), pygame.image.load("idle_down4.png"),
         pygame.image.load("idle_down5.png"), pygame.image.load("idle_down6.png"),
         pygame.image.load("idle_down7.png"), pygame.image.load("idle_down8.png")]

monster1 = pygame.image.load("monster1.png")

# Player Class
class player:
    def __init__(self, x, y, width, height, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.animation_numbers = 0
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.stop = True
        self.dammage = False

    def K(self, display):
        if self.health > 0:
            if self.animation_numbers + 1 > 49:
                self.animation_numbers = 0
            self.animation_numbers += 1
            if self.right:
                display.blit(pygame.transform.scale(walk_right[self.animation_numbers // 8], (80, 80)), (self.x, self.y))
            elif self.left:
                display.blit(pygame.transform.scale(pygame.transform.flip(walk_right[self.animation_numbers // 8], True, False), (80, 80)), (self.x, self.y))
            elif self.up:
                display.blit(pygame.transform.scale(walk_up[self.animation_numbers // 8], (80, 80)), (self.x, self.y))
            elif self.down:
                display.blit(pygame.transform.scale(pygame.transform.flip(walk_up[self.animation_numbers // 8], False, True), (80, 80)), (self.x, self.y))
            elif self.stop:
                display.blit(pygame.transform.scale(stand[self.animation_numbers // 9], (80, 80)), (self.x, self.y))
            self.right = False
            self.left = False
            self.up = False
            self.down = False
            self.stop = True
            self.healthbar(display)

    def healthbar(self, display):
        pygame.draw.rect(display, (255, 0, 0), (10, 10, 200, 10))  # Player's health bar on the left side
        pygame.draw.rect(display, (0, 255, 0), (10, 10, 200 * (self.health / 100), 10))

class Bullet:
    def __init__(self, x, y, target_x, target_y, damage, color, angle_off):
        self.x = x
        self.y = y
        self.speed = 10
        self.angle = math.atan2(y - target_y, x - target_x) + angle_off
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.damage = damage
        self.color = color

    def update(self):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), 5)

class Monster:
    def __init__(self, x, y, width, height, speed, health, shoot_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.shoot_type = shoot_type
        self.last_shot = 0
        self.phase = 1

    def draw(self, display):
        if self.health > 0:
            display.blit(pygame.transform.scale(monster1, (100, 100)), (self.x, self.y))
            self.healthbar(display)

    def healthbar(self, display):
        pygame.draw.rect(display, (255, 0, 0), (w - 310, 10, 300, 10))  # Monster's health bar
        pygame.draw.rect(display, (0, 255, 0), (w - 310, 10, 300 * (self.health / 300), 10))

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 200:
            direction_x = dx / distance
            direction_y = dy / distance
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed

    def shoot(self, player, current_time, monster_bullets):
        if current_time - self.last_shot > 1000:
            if self.phase == 1:
                bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, player.x, player.y, 10, (0, 0, 255), 0)
                monster_bullets.append(bullet)
            elif self.phase == 2:
                for i in range(12):
                    angle_offset = i * math.pi / 6
                    bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, player.x, player.y, 10, (0, 255, 0), angle_offset)
                    monster_bullets.append(bullet)
            self.last_shot = current_time

    def transition_phase(self):
        if self.health <= 0 and self.phase == 1:
            self.phase = 2
            self.health = 300


def Game():
    global player_bullets, monster_bullets
    fps = pygame.time.Clock()
    run = True
    while run:
        Screengame.blit(bg,(0,0))
        fps.tick(FPS)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if the_player.health > 0 and monster.health > 0:  # Only allow shooting if both are alive
                    player_bullets.append(Bullet(the_player.x + the_player.width // 2, the_player.y + the_player.height // 2, mouse_x, mouse_y, 10, (255, 0, 0), 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and the_player.x > 0:
            the_player.x -= 5
            the_player.left, the_player.stop = True, False
        if keys[pygame.K_d] and the_player.x + the_player.width < w:
            the_player.x += 5
            the_player.right, the_player.stop = True, False
        if keys[pygame.K_w] and the_player.y > 0:
            the_player.y -= 5
            the_player.up, the_player.stop = True, False
        if keys[pygame.K_s] and the_player.y + the_player.height < h:
            the_player.y += 5
            the_player.down, the_player.stop = True, False

        the_player.K(Screengame)
        monster.move(the_player)

        if the_player.health > 0 and monster.health > 0:
            monster.shoot(the_player, current_time, monster_bullets)

        monster.draw(Screengame)

        # Update and draw player bullets
        for bullet in player_bullets[:]:
            bullet.update()
            bullet.draw(Screengame)
            if pygame.Rect(monster.x, monster.y, monster.width, monster.height).colliderect(pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)):
                monster.health -= bullet.damage
                player_bullets.remove(bullet)
            elif bullet.x < 0 or bullet.x > w or bullet.y < 0 or bullet.y > h:
                player_bullets.remove(bullet)

        # Update and draw monster bullets
        for bullet in monster_bullets[:]:
            bullet.update()
            bullet.draw(Screengame)
            if pygame.Rect(the_player.x, the_player.y, the_player.width, the_player.height).colliderect(pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)):
                the_player.health -= bullet.damage
                monster_bullets.remove(bullet)
            elif bullet.x < 0 or bullet.x > w or bullet.y < 0 or bullet.y > h:
                monster_bullets.remove(bullet)

        monster.transition_phase()

        if monster.health <= 0 or the_player.health <= 0:
            font = pygame.font.SysFont(None, 55)
            text = "You Win!" if monster.health <= 0 else "Game Over!"
            message = font.render(f"{text} Press Q to quit.", True, (255, 255, 255))
            Screengame.blit(message, (w // 4, h // 2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    run = False

        pygame.display.update()


# Create Player and Monster objects
the_player = player(100, 100, 50, 50, 100)
monster = Monster(700, 100, 100, 100, 2, 300, 'single')
player_bullets = []
monster_bullets = []

# Run the Game
Game()
pygame.quit()
sys.exit()


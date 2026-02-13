import pygame
import random
import math

# --- Configuration & Initialization ---
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NEON VOID: Reloaded")
clock = pygame.time.Clock()

# --- Utility Functions ---

def pixel_art_to_surface(pattern, scale, color):
    """
    Converts a list of strings (strings of 'X' and '.') into a Pygame Surface.
    Allows for easy 'drawn' sprites without external image files.
    """
    rows = len(pattern)
    cols = len(pattern[0])
    # Create a surface with an alpha channel for transparency
    surf = pygame.Surface((cols * scale, rows * scale), pygame.SRCALPHA)
    for y, row in enumerate(pattern):
        for x, char in enumerate(row):
            if char == "X":
                # Draw a scaled rectangle for every 'X' in the pattern
                pygame.draw.rect(surf, color, (x * scale, y * scale, scale, scale))
    return surf

# Collision Layers (Bitmasking - prepared for advanced collision logic)
PLAYER_LAYER = 1 << 0
ENEMY_LAYER  = 1 << 1
BULLET_LAYER = 1 << 2
POWERUP_LAYER = 1 << 3

# --- Base Classes & Mixins ---

class Entity(pygame.sprite.Sprite):
    """Base class for all moving objects in the game."""
    def __init__(self, x, y, image, layer):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self._velocity = 3
        self.layer = layer

    @property
    def velocity(self):
        return self._velocity

class HealthMixin:
    """Reusable logic for any entity that has hit points."""
    def __init__(self, health):
        self.health = health

    def take_damage(self, amount):
        """Reduces health and returns True if the entity is destroyed."""
        self.health -= amount
        return self.health <= 0

class Particle(pygame.sprite.Sprite):
    """Simple circular particles for explosion effects."""
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (2, 2), 2)
        self.rect = self.image.get_rect(center=(x, y))
        # Random velocity for a 'burst' effect
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = random.randint(20, 40) # Lifetime in frames

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= 1
        if self.life <= 0:
            self.kill()

# --- Game Entities ---

PLAYER_SHIP_ART = [
    "....X....",
    "....X....",
    ".X.XXX.X.",
    ".X.XXX.X.",
    "XXXXXXXXX",
    "X..X.X..X",
    "X.......X",
]

class Player(Entity, HealthMixin):
    def __init__(self):
        image = pixel_art_to_surface(PLAYER_SHIP_ART, scale=4, color=(0, 200, 255))
        super().__init__(SCREEN_WIDTH // 2, 520, image, PLAYER_LAYER)
        HealthMixin.__init__(self, 100)
        self.cooldown = 0
        self.weapon_mode = "laser"
        self.weapon_timer = 0

    def move(self, dx):
        """Moves the player left/right and clamps within screen bounds."""
        self.rect.x += dx * self.velocity
        self.rect.x = max(self.rect.width // 2,
                          min(SCREEN_WIDTH - self.rect.width // 2, self.rect.x))

    def upgrade_weapon(self, new_mode, duration=600):
        """Temporarily changes the weapon type."""
        self.weapon_mode = new_mode
        self.weapon_timer = duration

    def update_weapon_timer(self):
        """Countdown for power-up duration."""
        if self.weapon_timer > 0:
            self.weapon_timer -= 1
            if self.weapon_timer == 0:
                self.weapon_mode = "laser" # Revert to default

class Bullet(Entity):
    def __init__(self, x, y, dx=0, dy=-8):
        image = pygame.Surface((4, 12), pygame.SRCALPHA)
        pygame.draw.rect(image, (255, 255, 0), (0, 0, 4, 12))
        super().__init__(x, y, image, BULLET_LAYER)
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom < 0:
            self.kill()

class PowerUp(Entity):
    def __init__(self, x, y, kind):
        color = (0, 255, 0) if kind == "heal" else (255, 165, 0)
        image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(image, color, (8, 8), 8)
        super().__init__(x, y, image, POWERUP_LAYER)
        self.kind = kind
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# --- Enemy Definitions ---

ENEMY_SHIP_ART = ["..X...X..","...XXX...",".XX.X.XX.","X.XXXXX.X","X.XXXXX.X",".XXXXXXX.","..X...X.."]
TANK_SHIP_ART = ["XXXXXXXXX","XXXXXXXXX","X.XXXXX.X","X..XXX..X","X...X...X",".X.....X.","..X...X.."]

class Enemy(Entity, HealthMixin):
    def __init__(self, x, y, enemy_type="standard"):
        # Setup stats based on enemy variety
        if enemy_type == "standard":
            art, color, self.speed, health = ENEMY_SHIP_ART, (255, 60, 60), 1.2, 30
        elif enemy_type == "zigzag":
            art, color, self.speed, health = ENEMY_SHIP_ART, (255, 100, 100), 1, 30
            self.angle = 0 # Used for math.sin movement
        elif enemy_type == "tank":
            art, color, self.speed, health = TANK_SHIP_ART, (255, 140, 0), 0.6, 60

        image = pixel_art_to_surface(art, scale=3, color=color)
        super().__init__(x, y, image, ENEMY_LAYER)
        HealthMixin.__init__(self, health)
        self.type = enemy_type

    def update(self):
        self.rect.y += self.speed
        if self.type == "zigzag":
            # Horizontal movement based on a Sine wave
            self.rect.x += int(3 * math.sin(self.angle))
            self.angle += 0.1
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# --- Wave & Spawning System ---

def formation_positions(center_x, start_y, formation_type, count, spacing=80):
    """Calculates coordinate points for different enemy spawn patterns."""
    positions = []
    if formation_type == "line":
        for i in range(count):
            x = center_x + (i - count // 2) * spacing
            y = start_y
            positions.append((x, y))
    elif formation_type == "v":
        for i in range(count):
            offset = i - count // 2
            x = center_x + offset * spacing
            y = start_y + abs(offset) * 40
            positions.append((x, y))
    elif formation_type == "swoop":
        for i in range(count):
            angle = i * (math.pi / (count - 1 if count > 1 else 1))
            x = center_x + int(240 * math.cos(angle))
            y = start_y + int(140 * math.sin(angle))
            positions.append((x, y))
    return positions

def prepare_wave():
    """Generates the data for the next wave of enemies."""
    global current_wave_enemies, spawn_index
    formation_type = random.choice(["line", "v", "swoop"])
    count = 6 + wave_number * 2
    positions = formation_positions(400, -120, formation_type, count)

    current_wave_enemies = []
    for pos in positions:
        # Weighted choice for enemy variety
        enemy_type = random.choices(["standard", "zigzag", "tank"], weights=[5, 3, 2])[0]
        current_wave_enemies.append((pos[0], pos[1], enemy_type))
    
    spawn_index = 0

# --- Game State Initialization ---

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
particles = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

score = 0
current_wave_enemies = []
spawn_timer = 0
spawn_delay = 45 # Frames between individual enemy spawns
spawn_index = 0
wave_number = 1

prepare_wave()

# Title Graphic
TITLE_ART = [
    "XX    XX  XXXXXX  XXXXXX  XX    XX",
    "XXX   XX  XX      XX  XX  XXX   XX",
    "XXXX  XX  XXXX    XX  XX  XXXX  XX",
    "XX XX XX  XX      XX  XX  XX XX XX",
    "XX  XXXX  XX      XX  XX  XX  XXXX",
    "XX   XXX  XX      XX  XX  XX   XXX",
    "XX    XX  XXXXXX  XXXXXX  XX    XX",
    "                                  ",
    "  XX  XX  XXXXXX  XX  XXXX    XXXX",
    "  XX  XX  XX  XX  XX  XX  XX  XX  ",
    "  XX  XX  XX  XX  XX  XX  XX  XXXX",
    "  XX  XX  XX  XX  XX  XX  XX  XX  ",
    "   XXXX   XXXXXX  XX  XXXX    XXXX"
]
title_surf = pixel_art_to_surface(TITLE_ART, scale=6, color=(0, 255, 255))
title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 250))

# Starfield Background
stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)] for _ in range(50)]

# --- Main Game Loop ---

running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if player.cooldown <= 0:
                mode = player.weapon_mode
                if mode == "laser":
                    bullet = Bullet(player.rect.centerx, player.rect.centery)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                elif mode == "spread":
                    for dx in (-2, 0, 2): # Shoots 3 bullets at different angles
                        bullet = Bullet(player.rect.centerx + dx*8, player.rect.centery, dx, -5)
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                elif mode == "charge":
                    # Placeholder for charge shot logic
                    bullet = Bullet(player.rect.centerx, player.rect.centery)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                
                player.cooldown = 15

    # 2. Input Processing (Continuous movement)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1)
    if keys[pygame.K_RIGHT]:
        player.move(1)

    # 3. Update Logic
    all_sprites.update()
    player.update_weapon_timer()
    
    # --- Collision: Bullets vs Enemies ---
    for bullet in bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in hits:
            if enemy.take_damage(20):
                score += 10
                # Spawn explosion particles
                for _ in range(12):
                    p = Particle(enemy.rect.centerx, enemy.rect.centery, (255, 50, 50))
                    particles.add(p)
                    all_sprites.add(p)
                
                # Chance to drop a PowerUp
                if random.random() < 0.35:
                    kind = random.choice(["heal", "weapon"])
                    pu = PowerUp(enemy.rect.centerx, enemy.rect.centery, kind)
                    powerups.add(pu)
                    all_sprites.add(pu)
                
                enemy.kill()
            bullet.kill() # Bullet dies on impact
    
    # --- Collision: Player vs Enemies ---
    player_hits = pygame.sprite.spritecollide(player, enemies, True)
    if player_hits:
        if player.take_damage(20):
             running = False # Game Over logic

    # --- Collision: PowerUps ---
    pu_hits = pygame.sprite.spritecollide(player, powerups, True)
    for pu in pu_hits:
        if pu.kind == "heal":
            player.health = min(100, player.health + 25)
        elif pu.kind == "weapon":
            new_weapon = random.choice(["spread", "charge"])
            player.upgrade_weapon(new_weapon)

    # --- Spawning Logic ---
    spawn_timer += 1
    if spawn_timer >= spawn_delay and spawn_index < len(current_wave_enemies):
        x, y, etype = current_wave_enemies[spawn_index]
        enemy = Enemy(x, y, etype)
        enemies.add(enemy)
        all_sprites.add(enemy)
        spawn_index += 1
        spawn_timer = 0

    # If all enemies in wave are spawned and killed, start next wave
    if spawn_index >= len(current_wave_enemies) and not enemies:
        wave_number += 1
        prepare_wave()

    if player.cooldown > 0:
        player.cooldown -= 1

    # 4. Drawing
    screen.fill((5, 5, 30)) # Dark space blue

    # Update and Draw Starfield
    for star in stars:
        pygame.draw.circle(screen, (200, 200, 200), star, 1)
        star[1] = (star[1] + 1.5) % SCREEN_HEIGHT # Stars wrap around screen

    all_sprites.draw(screen)
    screen.blit(title_surf, title_rect) # Draw the "Neon Void" logo

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
import pgzrun
import random
from enum import Enum


# Constants
WIDTH = 800
HEIGHT = 600
TITLE = "Plataforma - Aventura"

GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 4
ENEMY_SPEED = 2


class GameState(Enum):
    """Game states enumeration"""
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3


class AnimatedSprite:
    """Base class for animated sprites"""
    
    def __init__(self, x, y, images, animation_speed=0.2):
        self.x = x
        self.y = y
        self.images = images
        self.current_frame = 0
        self.animation_speed = animation_speed
        self.animation_timer = 0
        self.width = 40
        self.height = 40
        
    def animate(self, dt):
        """Update animation frame"""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
    
    def get_rect(self):
        """Get collision rectangle"""
        return Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        """Draw sprite with current animation frame"""
        screen.draw.filled_rect(
            self.get_rect(),
            self.images[self.current_frame]
        )


class Player(AnimatedSprite):
    """Player character with jump mechanics"""
    
    def __init__(self, x, y):
        # Animation colors (simulating sprite frames)
        idle_colors = ['blue', 'darkblue', 'blue']
        super().__init__(x, y, idle_colors, 0.15)
        
        self.velocity_y = 0
        self.is_on_ground = False
        self.facing_right = True
        
    def update(self, dt, platforms):
        """Update player physics and position"""
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Check ground collision
        self.is_on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                if self.velocity_y > 0:  # Falling
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.is_on_ground = True
        
        # Keep player in bounds
        if self.y > HEIGHT:
            return False  # Player fell off
        
        self.animate(dt)
        return True
    
    def jump(self):
        """Make player jump"""
        if self.is_on_ground:
            self.velocity_y = JUMP_STRENGTH
    
    def move_left(self):
        """Move player left"""
        self.x -= PLAYER_SPEED
        self.facing_right = False
        if self.x < 0:
            self.x = 0
    
    def move_right(self):
        """Move player right"""
        self.x += PLAYER_SPEED
        self.facing_right = True
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
    
    def check_collision(self, other):
        """Check collision with another object"""
        return self.get_rect().colliderect(other.get_rect())


class Enemy(AnimatedSprite):
    """Enemy that moves on platforms"""
    
    def __init__(self, x, y, platform):
        # Animation colors (simulating sprite frames)
        enemy_colors = ['red', 'darkred', 'orangered', 'darkred']
        super().__init__(x, y, enemy_colors, 0.12)
        
        self.platform = platform
        self.direction = random.choice([-1, 1])
        self.velocity_y = 0
        
    def update(self, dt):
        """Update enemy movement"""
        # Move horizontally on platform
        self.x += ENEMY_SPEED * self.direction
        
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Check platform boundaries
        platform_rect = self.platform.get_rect()
        if self.x <= platform_rect.left or self.x + self.width >= platform_rect.right:
            self.direction *= -1
        
        # Keep on platform
        if self.y + self.height >= self.platform.y:
            self.y = self.platform.y - self.height
            self.velocity_y = 0
        
        self.animate(dt)


class Platform:
    """Static platform object"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = 'green'
    
    def get_rect(self):
        """Get platform rectangle"""
        return Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        """Draw platform"""
        screen.draw.filled_rect(self.get_rect(), self.color)


class Button:
    """Clickable menu button"""
    
    def __init__(self, x, y, width, height, text, color='gray'):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = 'lightgray'
        self.is_hovered = False
    
    def update(self, mouse_pos):
        """Update button hover state"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self):
        """Draw button"""
        color = self.hover_color if self.is_hovered else self.color
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(
            self.text,
            center=(self.rect.centerx, self.rect.centery),
            fontsize=30,
            color='white'
        )
    
    def is_clicked(self, mouse_pos):
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos)


class Game:
    """Main game controller"""
    
    def __init__(self):
        self.state = GameState.MENU
        self.sound_enabled = True
        self.music_playing = False
        
        # Menu buttons
        self.start_button = Button(300, 200, 200, 60, "Iniciar Jogo")
        self.sound_button = Button(300, 280, 200, 60, "Som: ON")
        self.exit_button = Button(300, 360, 200, 60, "Sair")
        
        self.reset_game()
    
    def reset_game(self):
        """Reset game entities"""
        # Create platforms
        self.platforms = [
            Platform(0, 550, 800, 50),           # Ground
            Platform(150, 450, 150, 20),         # Platform 1
            Platform(400, 350, 150, 20),         # Platform 2
            Platform(100, 250, 150, 20),         # Platform 3
            Platform(500, 200, 150, 20),         # Platform 4
        ]
        
        # Create player
        self.player = Player(50, 400)
        
        # Create enemies on platforms
        self.enemies = [
            Enemy(160, 410, self.platforms[1]),
            Enemy(410, 310, self.platforms[2]),
            Enemy(510, 160, self.platforms[4]),
        ]
        
        self.game_over = False
        self.score = 0
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        self.sound_button.text = f"Som: {'ON' if self.sound_enabled else 'OFF'}"
        
        # Note: Actual sound implementation would go here
        # For this educational example, we're simulating sound controls
    
    def update(self, dt):
        """Update game logic"""
        if self.state == GameState.PLAYING:
            # Update player
            if not self.player.update(dt, self.platforms):
                self.game_over = True
                self.state = GameState.GAME_OVER
            
            # Update enemies
            for enemy in self.enemies:
                enemy.update(dt)
                
                # Check collision with player
                if self.player.check_collision(enemy):
                    self.game_over = True
                    self.state = GameState.GAME_OVER
            
            # Increase score over time
            self.score += 1
    
    def draw(self):
        """Draw game elements"""
        screen.clear()
        screen.fill('skyblue')
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
    
    def draw_menu(self):
        """Draw main menu"""
        screen.draw.text(
            TITLE,
            center=(WIDTH // 2, 100),
            fontsize=50,
            color='darkblue'
        )
        
        self.start_button.draw()
        self.sound_button.draw()
        self.exit_button.draw()
    
    def draw_game(self):
        """Draw game scene"""
        # Draw platforms
        for platform in self.platforms:
            platform.draw()
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw()
        
        # Draw player
        self.player.draw()
        
        # Draw score
        screen.draw.text(
            f"Pontuação: {self.score}",
            (10, 10),
            fontsize=30,
            color='white'
        )
        
        # Draw instructions
        screen.draw.text(
            "Setas direcionais [<-] [->] Mover | Espaço: Pular",
            (10, HEIGHT - 30),
            fontsize=20,
            color='white'
        )
    
    def draw_game_over(self):
        """Draw game over screen"""
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=60,
            color='red'
        )
        
        screen.draw.text(
            f"Final Score: {self.score}",
            center=(WIDTH // 2, HEIGHT // 2 + 20),
            fontsize=40,
            color='white'
        )
        
        screen.draw.text(
            "Press ENTER to return to menu",
            center=(WIDTH // 2, HEIGHT // 2 + 80),
            fontsize=25,
            color='white'
        )


# Global game instance
game = Game()


def update(dt):
    """PgZero update function"""
    game.update(dt)


def draw():
    """PgZero draw function"""
    game.draw()


def on_mouse_move(pos):
    """Handle mouse movement"""
    if game.state == GameState.MENU:
        game.start_button.update(pos)
        game.sound_button.update(pos)
        game.exit_button.update(pos)


def on_mouse_down(pos):
    """Handle mouse clicks"""
    if game.state == GameState.MENU:
        if game.start_button.is_clicked(pos):
            game.reset_game()
            game.state = GameState.PLAYING
        elif game.sound_button.is_clicked(pos):
            game.toggle_sound()
        elif game.exit_button.is_clicked(pos):
            exit()


def on_key_down(key):
    """Handle key presses"""
    if game.state == GameState.PLAYING:
        if key == keys.SPACE:
            game.player.jump()
    
    elif game.state == GameState.GAME_OVER:
        if key == keys.RETURN:
            game.state = GameState.MENU


def on_key_up(key):
    """Handle key releases"""
    pass


# Handle continuous key presses
def handle_keyboard():
    """Handle held-down keys"""
    if game.state == GameState.PLAYING:
        if keyboard.left:
            game.player.move_left()
        if keyboard.right:
            game.player.move_right()


# Override update to include keyboard handling
_original_update = update
def update(dt):
    handle_keyboard()
    _original_update(dt)


# Run game
pgzrun.go()

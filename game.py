import pgzrun
import random
from enum import Enum
import os
import pygame  # Necessário para transformar (escalar/virar) a imagem

from pgzero import music
from pgzero.keyboard import keyboard
from pgzero.loaders import sounds
from pgzero.rect import Rect
from pgzero.actor import Actor

# Constantes do jogo
WIDTH = 800
HEIGHT = 600
TITLE = "Plataforma - Aventura do Jacaré"

# Centralizar janela na tela
os.environ['SDL_VIDEO_CENTERED'] = '1'

GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 4
ENEMY_SPEED = 2

ENEMY_SPRITE = 'jacare/jacare.png'

class GameState(Enum):
    """Enumeração dos estados do jogo"""
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3


class AnimatedSprite:
    """Classe base para sprites animados (usada pelo Player)"""

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
        """Atualiza o frame da animação"""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)

    def get_rect(self):
        """Obtém o retângulo de colisão"""
        return Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """Desenha o sprite com o frame atual da animação"""
        screen.draw.filled_rect(
            self.get_rect(),
            self.images[self.current_frame]
        )


class Player(AnimatedSprite):
    """Personagem do jogador com mecânica de pulo"""

    def __init__(self, x, y):
        # Cores da animação (simulando frames de sprite)
        idle_colors = ['blue', 'darkblue', 'blue']
        super().__init__(x, y, idle_colors, 0.15)

        self.velocity_y = 0
        self.is_on_ground = False
        self.facing_right = True
        self.jump_pressed = False

    def update(self, dt, platforms):
        """Atualiza a física e posição do jogador"""
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.is_on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                if self.velocity_y > 0:  # Caindo
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.is_on_ground = True

        if self.y > HEIGHT:
            return False

        self.animate(dt)
        return True

    def jump(self):
        if self.is_on_ground and not self.jump_pressed:
            self.velocity_y = JUMP_STRENGTH
            self.is_on_ground = False
            self.jump_pressed = True
            return True
        return False

    def release_jump(self):
        self.jump_pressed = False

    def move_left(self):
        self.x -= PLAYER_SPEED
        self.facing_right = False
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += PLAYER_SPEED
        self.facing_right = True
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

    def check_collision(self, other):
        return self.get_rect().colliderect(other.get_rect())


class Enemy:
    """
    Inimigo Jacaré - Refatorado para corrigir a direção do olhar
    """

    def __init__(self, x, y, platform):
        self.x = x
        self.y = y
        self.platform = platform
        self.direction = random.choice([-1, 1])
        self.velocity_y = 0

        # Dimensões do inimigo
        self.width = 50
        self.height = 50

        # Carrega o ator com a imagem 'jacare' (deve estar na pasta images/)
        try:
            self.actor = Actor(ENEMY_SPRITE)

            # Ajusta o tamanho da imagem para 50x50
            original_surf = self.actor._surf
            self.actor._surf = pygame.transform.scale(original_surf, (self.width, self.height))

            # Guardamos a imagem original escalada para poder virar (flip) depois
            self.base_surf = self.actor._surf

        except Exception as e:
            print(f"Erro ao carregar sprite jacare: {e}")
            self.actor = None

    def update(self, dt):
        """Atualiza o movimento do inimigo"""
        # Move horizontalmente
        self.x += ENEMY_SPEED * self.direction

        # Aplica gravidade
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # Verifica limites da plataforma
        platform_rect = self.platform.get_rect()
        # Se bater na borda esquerda ou direita da plataforma, inverte a direção
        if self.x <= platform_rect.left:
            self.direction = 1  # Força ir para direita
        elif self.x + self.width >= platform_rect.right:
            self.direction = -1  # Força ir para esquerda

        # Mantém na plataforma (colisão com o chão)
        if self.y + self.height >= self.platform.y:
            self.y = self.platform.y - self.height
            self.velocity_y = 0

        # Atualiza a posição do Actor e a direção do olhar
        if self.actor:
            self.actor.topleft = (self.x, self.y)

            # --- CORREÇÃO AQUI ---
            # Lógica invertida:
            # Se a direção for 1 (Direita), is_flipped será True (vira para direita).
            # Se a direção for -1 (Esquerda), is_flipped será False (mantém original/esquerda).
            # Nota: Isso assume que sua imagem original 'jacare.png' aponta para a ESQUERDA.
            # Se a imagem apontar para a DIREITA, inverta para: (self.direction == -1)

            is_flipped = (self.direction == 1)

            self.actor._surf = pygame.transform.flip(self.base_surf, is_flipped, False)

    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """Desenha o ator na tela"""
        if self.actor:
            self.actor.draw()
        else:
            screen.draw.filled_rect(self.get_rect(), 'red')


class Platform:
    """Objeto de plataforma estática"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = 'green'

    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        screen.draw.filled_rect(self.get_rect(), self.color)


class Button:
    """Botão clicável do menu"""

    def __init__(self, x, y, width, height, text, color='gray'):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = 'lightgray'
        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(
            self.text,
            center=(self.rect.centerx, self.rect.centery),
            fontsize=30,
            color='white'
        )

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Game:
    """Controlador principal do jogo"""

    def __init__(self):
        self.state = GameState.MENU
        self.sound_enabled = True
        self.music_playing = False

        self.start_button = Button(300, 200, 200, 60, "Iniciar Jogo")
        self.sound_button = Button(300, 280, 200, 60, "Som: ON")
        self.exit_button = Button(300, 360, 200, 60, "Sair")

        self.reset_game()

    def reset_game(self):
        self.platforms = [
            Platform(0, 550, 800, 50),  # Chão
            Platform(150, 450, 150, 20),
            Platform(400, 350, 150, 20),
            Platform(100, 250, 150, 20),
            Platform(500, 200, 150, 20),
        ]

        self.player = Player(50, 400)

        self.enemies = [
            Enemy(160, 410, self.platforms[1]),
            Enemy(410, 310, self.platforms[2]),
            Enemy(510, 160, self.platforms[4]),
            Enemy(250, 510, self.platforms[0]),
            Enemy(600, 510, self.platforms[0]),
        ]

        self.game_over = False
        self.score = 0

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_button.text = f"Som: {'ON' if self.sound_enabled else 'OFF'}"
        if self.sound_enabled and self.state == GameState.PLAYING:
            self.play_music()
        else:
            self.stop_music()

    def play_music(self):
        if self.sound_enabled and not self.music_playing:
            try:
                music.play('background')
                self.music_playing = True
            except:
                pass

    def stop_music(self):
        try:
            music.stop()
            self.music_playing = False
        except:
            pass

    def play_sound(self, sound_name):
        if self.sound_enabled:
            try:
                sounds[sound_name].play()
            except:
                pass

    def start_game(self):
        self.reset_game()
        self.state = GameState.PLAYING
        self.play_music()

    def update(self, dt):
        if self.state == GameState.PLAYING:
            if not self.player.update(dt, self.platforms):
                self.game_over = True
                self.state = GameState.GAME_OVER
                self.stop_music()
                self.play_sound('game_over')

            for enemy in self.enemies:
                enemy.update(dt)
                if self.player.check_collision(enemy):
                    self.game_over = True
                    self.state = GameState.GAME_OVER
                    self.stop_music()
                    self.play_sound('game_over')

            self.score += 1

    def draw(self):
        screen.clear()
        screen.fill('skyblue')

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

    def draw_menu(self):
        screen.draw.text(
            TITLE,
            center=(WIDTH // 2, 100),
            fontsize=50,
            color='darkblue'
        )
        self.start_button.draw()
        self.sound_button.draw()
        self.exit_button.draw()
        screen.draw.text(
            "Sobreviva o máximo possível!",
            center=(WIDTH // 2, 460),
            fontsize=25,
            color='white'
        )

    def draw_game(self):
        for platform in self.platforms:
            platform.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()

        screen.draw.text(f"Pontuação: {self.score}", (10, 10), fontsize=30, color='white')
        screen.draw.text(f"Inimigos: {len(self.enemies)}", (10, 45), fontsize=25, color='white')
        screen.draw.text(
            "Setas direcionais [<-] [->] Mover | Espaço: Pular",
            (10, HEIGHT - 30),
            fontsize=20,
            color='white'
        )

    def draw_game_over(self):
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=60,
            color='red'
        )
        screen.draw.text(
            f"Pontuação Final: {self.score}",
            center=(WIDTH // 2, HEIGHT // 2 + 20),
            fontsize=40,
            color='white'
        )
        screen.draw.text(
            "Pressione ENTER para voltar ao menu",
            center=(WIDTH // 2, HEIGHT // 2 + 80),
            fontsize=25,
            color='white'
        )


game = Game()


def update(dt):
    game.update(dt)


def draw():
    game.draw()


def on_mouse_move(pos):
    if game.state == GameState.MENU:
        game.start_button.update(pos)
        game.sound_button.update(pos)
        game.exit_button.update(pos)


def on_mouse_down(pos):
    if game.state == GameState.MENU:
        if game.start_button.is_clicked(pos):
            game.start_game()
        elif game.sound_button.is_clicked(pos):
            game.toggle_sound()
        elif game.exit_button.is_clicked(pos):
            exit()


def on_key_down(key):
    if game.state == GameState.PLAYING:
        if key == keys.SPACE:
            if game.player.jump():
                game.play_sound('jump')
    elif game.state == GameState.GAME_OVER:
        if key == keys.RETURN:
            game.state = GameState.MENU
            game.stop_music()


def on_key_up(key):
    if game.state == GameState.PLAYING:
        if key == keys.SPACE:
            game.player.release_jump()


def handle_keyboard():
    if game.state == GameState.PLAYING:
        if keyboard.left:
            game.player.move_left()
        if keyboard.right:
            game.player.move_right()


_original_update = update


def update(dt):
    handle_keyboard()
    _original_update(dt)


pgzrun.go()
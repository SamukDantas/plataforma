import pgzrun
import random
import os
from enum import Enum

# Necessário para transformar (escalar/virar) o sprite, pois o PGZero não faz de modo nativo
from pygame.transform import scale
from pygame.transform import flip

from pgzero import music
from pgzero.keyboard import keyboard
from pgzero.loaders import sounds
from pgzero.rect import Rect
from pgzero.actor import Actor

# ============================================
# CONSTANTES DO JOGO
# ============================================
WIDTH = 800
HEIGHT = 600
TITLE = "Plataforma - Aventura do Jacaré"

# Centralizar janela na tela
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Física
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 4
ENEMY_SPEED = 2

# Sprites
ENEMY_SPRITE = 'jacare/jacare.png'
PLAYER_SPRITE_IDLE = 'mini_homem/mini_homem_parado'
PLAYER_SPRITE_RUNNING = 'mini_homem/mini_homem_correndo'
PLAYER_SPRITE_JUMPING = 'mini_homem/mini_homem_pulando'


# ============================================
# ENUMERAÇÕES
# ============================================
class GameState(Enum):
    """Estados possíveis do jogo"""
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3


# ============================================
# CLASSE PLAYER
# ============================================
class Player:
    """
    Personagem do jogador com mecânica de pulo e múltiplos sprites.
    Usa PgZero + pygame mínimo (apenas para scale e flip).
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40

        # Física
        self.velocity_y = 0
        self.is_on_ground = False
        self.facing_right = True
        self.jump_pressed = False
        self.is_moving_horizontal = False

        # Sistema de Sprites
        try:
            # Carrega os três sprites base
            idle_actor = Actor(PLAYER_SPRITE_IDLE)
            run_actor = Actor(PLAYER_SPRITE_RUNNING)
            jump_actor = Actor(PLAYER_SPRITE_JUMPING)

            # Escala para o tamanho do hitbox
            self.surf_idle = scale(idle_actor._surf, (self.width, self.height))
            self.surf_run = scale(run_actor._surf, (self.width, self.height))
            self.surf_jump = scale(jump_actor._surf, (self.width, self.height))

            # Actor principal
            self.actor = Actor(PLAYER_SPRITE_IDLE)
            self.actor._surf = self.surf_idle
            self.sprites_loaded = True
        except Exception as e:
            print(f"Erro ao carregar sprites do jogador: {e}")
            self.sprites_loaded = False

    def update(self, dt, platforms):
        """
        Atualiza a física, posição e escolhe o sprite correto.
        Retorna False se o jogador caiu fora da tela.
        """
        # Aplica gravidade
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # Verifica colisão com plataformas
        self.is_on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                if self.velocity_y > 0:  # Está caindo
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.is_on_ground = True

        # Verificação adicional: se está muito próximo de uma plataforma, considera no chão
        # Isso resolve problemas de timing entre física e renderização
        if not self.is_on_ground:
            for platform in platforms:
                distance_to_platform = platform.y - (self.y + self.height)
                if -3 <= distance_to_platform <= 3:
                    player_left = self.x
                    player_right = self.x + self.width
                    platform_left = platform.x
                    platform_right = platform.x + platform.width

                    if player_right > platform_left and player_left < platform_right:
                        self.is_on_ground = True
                        self.y = platform.y - self.height
                        if self.velocity_y > 0:
                            self.velocity_y = 0
                        break

        # Verifica se caiu fora da tela
        if self.y > HEIGHT:
            return False

        # Atualização do sprite baseado no estado
        if self.sprites_loaded:
            # 1. Escolhe a superfície base
            if not self.is_on_ground:
                # Se não está no chão, está pulando/caindo
                base_surf = self.surf_jump
            elif self.is_moving_horizontal:
                # Se está no chão e se movendo horizontalmente
                base_surf = self.surf_run
            else:
                # Está no chão e parado
                base_surf = self.surf_idle

            # 2. Aplicar espelhamento (flip) baseado na direção
            # Se NÃO está olhando para direita, flip = True
            is_flipped = not self.facing_right
            final_surf = flip(base_surf, is_flipped, False)

            # 3. Atualiza o actor
            self.actor._surf = final_surf
            self.actor.topleft = (self.x, self.y)

        # Reseta a flag de movimento
        self.is_moving_horizontal = False

        return True

    def jump(self):
        """Executa o pulo se estiver no chão. Retorna True se pulou."""
        if self.is_on_ground and not self.jump_pressed:
            self.velocity_y = JUMP_STRENGTH
            self.is_on_ground = False
            self.jump_pressed = True
            return True
        return False

    def release_jump(self):
        """Libera a tecla de pulo"""
        self.jump_pressed = False

    def move_left(self):
        """Move o jogador para a esquerda"""
        self.x -= PLAYER_SPEED
        self.facing_right = False
        self.is_moving_horizontal = True
        if self.x < 0:
            self.x = 0

    def move_right(self):
        """Move o jogador para a direita"""
        self.x += PLAYER_SPEED
        self.facing_right = True
        self.is_moving_horizontal = True
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, other):
        """Verifica colisão"""
        return self.get_rect().colliderect(other.get_rect())

    def draw(self):
        """Desenha o sprite"""
        if self.sprites_loaded:
            self.actor.draw()
        else:
            screen.draw.filled_rect(self.get_rect(), 'blue')


# ============================================
# CLASSE ENEMY
# ============================================
class Enemy:
    """Inimigo Jacaré que patrulha uma plataforma"""

    def __init__(self, x, y, platform):
        self.x = x
        self.y = y
        self.platform = platform
        self.direction = random.choice([-1, 1])
        self.velocity_y = 0
        self.width = 50
        self.height = 50

        try:
            enemy_actor = Actor(ENEMY_SPRITE)
            self.base_surf = scale(enemy_actor._surf, (self.width, self.height))
            self.actor = Actor(ENEMY_SPRITE)
            self.actor._surf = self.base_surf
            self.sprites_loaded = True
        except Exception as e:
            print(f"Erro ao carregar sprite jacare: {e}")
            self.sprites_loaded = False

    def update(self, dt):
        """Atualiza movimento do inimigo"""
        # Movimento horizontal
        self.x += ENEMY_SPEED * self.direction

        # Aplica gravidade
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # Verifica limites da plataforma
        platform_rect = self.platform.get_rect()
        if self.x <= platform_rect.left:
            self.direction = 1
        elif self.x + self.width >= platform_rect.right:
            self.direction = -1

        # Mantém na plataforma
        if self.y + self.height >= self.platform.y:
            self.y = self.platform.y - self.height
            self.velocity_y = 0

        # Atualiza sprite
        if self.sprites_loaded:
            self.actor.topleft = (self.x, self.y)
            # Assumindo que a imagem original olha para a ESQUERDA.
            # Se direção for 1 (Direita), vira (True).
            is_flipped = (self.direction == 1)
            self.actor._surf = flip(self.base_surf, is_flipped, False)

    def get_rect(self):
        """Retorna retângulo de colisão"""
        return Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """Desenha o inimigo"""
        if self.sprites_loaded:
            self.actor.draw()
        else:
            screen.draw.filled_rect(self.get_rect(), 'red')


# ============================================
# CLASSE PLATFORM
# ============================================
class Platform:
    """Plataforma estática"""

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


# ============================================
# CLASSE BUTTON
# ============================================
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


# ============================================
# CLASSE GAME
# ============================================
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
            Platform(0, 550, 800, 50),
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
            # O update do player agora cuida da troca de sprites
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
        screen.draw.text(TITLE, center=(WIDTH // 2, 100), fontsize=50, color='darkblue')
        self.start_button.draw()
        self.sound_button.draw()
        self.exit_button.draw()
        screen.draw.text("Sobreviva o máximo possível!", center=(WIDTH // 2, 460), fontsize=25, color='white')

    def draw_game(self):
        for platform in self.platforms:
            platform.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()

        screen.draw.text(f"Pontuação: {self.score}", (10, 10), fontsize=30, color='white')
        screen.draw.text(f"Inimigos: {len(self.enemies)}", (10, 45), fontsize=25, color='white')
        screen.draw.text("Setas direcionais [<-] [->] Mover | Espaço: Pular", (10, HEIGHT - 30), fontsize=20,
                         color='white')

    def draw_game_over(self):
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=60, color='red')
        screen.draw.text(f"Pontuação Final: {self.score}", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=40,
                         color='white')
        screen.draw.text("Pressione ENTER para voltar ao menu", center=(WIDTH // 2, HEIGHT // 2 + 80), fontsize=25,
                         color='white')


# ============================================
# INICIALIZAÇÃO
# ============================================
game = Game()


# ============================================
# EVENTOS
# ============================================
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
    # Esta função é chamada em cada frame antes do update principal
    if game.state == GameState.PLAYING:
        if keyboard.left:
            game.player.move_left()
        if keyboard.right:
            game.player.move_right()


def update(dt):
    handle_keyboard()
    game.update(dt)


def draw():
    game.draw()


pgzrun.go()
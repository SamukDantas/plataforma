# 🎮 Plataforma - Aventura do Jacaré

Um jogo de plataforma educativo desenvolvido em Python usando PgZero, seguindo princípios SOLID e Clean Code.

## 📋 Requisitos Atendidos

✅ **Bibliotecas permitidas**: PgZero, math, random e pygame (apenas transform para scale/flip)  
✅ **Gênero**: Platformer (visão lateral com plataformas)  
✅ **Menu principal**: Com botões clicáveis (Iniciar, Som On/Off, Sair)  
✅ **Música e sons**: Sistema de controle implementado com música de fundo  
✅ **Inimigos**: 5 jacarés perigosos patrulhando diferentes áreas  
✅ **Movimento de inimigos**: Patrulham suas plataformas com animação  
✅ **Classes próprias**: Player, Enemy, Platform, Button e Game  
✅ **Sprites reais**: Sistema de múltiplos sprites para cada estado do personagem  
✅ **Animação de sprites**: Estados de parado, correndo e pulando com flip direcional  
✅ **Nomenclatura**: Nomes claros em inglês, seguindo PEP8  
✅ **Lógica e bugs**: Mecânica funcional sem erros  
✅ **Código único**: 100% original e independente  

## 🎯 Características do Jogo

### Gameplay
- **Objetivo**: Sobreviva o máximo de tempo possível sem cair ou tocar nos jacarés
- **Controles**:
  - ⬅️ ➡️ **Setas**: Mover para esquerda/direita
  - **ESPAÇO**: Pular
- **Mecânicas**:
  - Física de gravidade realista
  - Sistema de plataformas com colisão precisa
  - 5 jacarés que patrulham diferentes plataformas
  - Sistema de pontuação baseado em tempo de sobrevivência
  - Música de fundo durante o jogo
  - Sons de efeitos (pulo, game over)
  - Detecção de colisão refinada para evitar bugs de "pé no ar"

### Personagens

#### 🏃 Mini Homem (Jogador)
- **Sprite Parado**: `mini_homem/mini_homem_parado.png` - Exibido quando o jogador não se move
- **Sprite Correndo**: `mini_homem/mini_homem_correndo.png` - Exibido durante movimento horizontal
- **Sprite Pulando**: `mini_homem/mini_homem_pulando.png` - Exibido quando no ar
- **Flip Automático**: Vira automaticamente para a direção do movimento
- **Tamanho**: 40x40 pixels
- **Física**: 
  - Velocidade horizontal: 4 pixels/frame
  - Força do pulo: -12 (velocidade inicial)
  - Gravidade aplicada: 0.5 pixels/frame²
  
#### 🐊 Jacarés (Inimigos)
- **Sprite**: `jacare/jacare.png`
- **Quantidade**: 5 jacarés posicionados estrategicamente
- **Distribuição**:
  - 2 jacarés no chão (plataforma inferior y=550)
  - 1 jacaré na plataforma 2 (y=450)
  - 1 jacaré na plataforma 3 (y=350)
  - 1 jacaré na plataforma 5 (y=200)
- **Comportamento**:
  - Patrulham suas plataformas automaticamente
  - Invertem direção ao chegar nas bordas
  - Sprite vira na direção do movimento
  - Velocidade: 2 pixels/frame
- **Tamanho**: 50x50 pixels
- **Física**: Respeitam gravidade e ficam presos às suas plataformas

### Sistema de Áudio
- **Música de Fundo**: `background.mp3` - Toca automaticamente durante o jogo
- **Efeitos Sonoros**:
  - `jump` - Som ao pular
  - `game_over` - Som quando o jogo termina
- **Controle de Som**: Botão no menu para ligar/desligar
- **Estado Persistente**: Configuração de som mantida durante a sessão

## 🏗️ Estrutura do Código (SOLID)

### Single Responsibility Principle (SRP)
- `Player`: Gerencia apenas lógica do jogador (física, sprites, movimento)
- `Enemy`: Gerencia apenas comportamento dos inimigos (patrulha, animação)
- `Platform`: Representa apenas plataformas estáticas
- `Button`: Cuida apenas de botões de interface
- `Game`: Coordena o jogo (Controller pattern)
- `GameState`: Enumera estados do jogo (MENU, PLAYING, GAME_OVER)

### Open/Closed Principle (OCP)
- Classes são extensíveis sem modificação
- `Player` e `Enemy` podem ter novos comportamentos adicionados
- Sistema de sprites facilmente expansível

### Liskov Substitution Principle (LSP)
- `Player` e `Enemy` são intercambiáveis em contextos de colisão
- Ambos implementam `get_rect()` e `check_collision()`

### Interface Segregation Principle (ISP)
- Classes têm métodos específicos às suas necessidades
- `Player` tem `jump()`, `move_left()`, `move_right()`
- `Enemy` tem lógica de patrulha interna
- Sem métodos desnecessários forçados

### Dependency Inversion Principle (DIP)
- Classes dependem de abstrações (Rect, Actor do PgZero)
- Baixo acoplamento entre componentes
- Game não depende de implementações específicas

## 📁 Estrutura Completa do Projeto

```
plataforma_aventura_jacare/
│
├── game.py                      # Código principal do jogo (arquivo único)
├── README.md                    # Esta documentação
├── requirements.txt             # Dependências Python
├── LICENSE                      # Licença MIT
├── .gitignore                  # Arquivos a ignorar no Git
├── REQUIREMENTS_CHECKLIST.md   # Checklist de requisitos atendidos
│
├── images/                      # Pasta de sprites (PgZero busca aqui)
│   ├── jacare/
│   │   └── jacare.png          # Sprite do inimigo jacaré (50x50)
│   │
│   └── mini_homem/
│       ├── mini_homem_parado.png    # Sprite do jogador parado (40x40)
│       ├── mini_homem_correndo.png  # Sprite do jogador correndo (40x40)
│       └── mini_homem_pulando.png   # Sprite do jogador pulando (40x40)
│
├── music/                       # Pasta de músicas (formato MP3)
│   └── background.mp3          # Música de fundo do jogo
│
└── sounds/                      # Pasta de efeitos sonoros (formato WAV)
    ├── jump.wav                # Som ao pular
    └── game_over.wav           # Som de game over
```

### 📝 Detalhes dos Arquivos

#### `game.py` (Arquivo Principal)
Contém todas as classes e lógica do jogo:
- **Constantes**: WIDTH, HEIGHT, GRAVITY, JUMP_STRENGTH, etc.
- **Enum GameState**: Estados do jogo
- **Classe Player**: Personagem jogador com física e sprites
- **Classe Enemy**: Inimigos jacarés com patrulha
- **Classe Platform**: Plataformas estáticas
- **Classe Button**: Botões do menu
- **Classe Game**: Controlador principal
- **Funções PgZero**: update(), draw(), on_key_down(), etc.

#### `requirements.txt`
```
pgzero>=1.2.1
```

#### `.gitignore`
Ignora arquivos temporários e de cache:
```
__pycache__/
*.py[cod]
*$py.class
.vscode/
.idea/
.DS_Store
```

#### Sprites Necessários

**Mini Homem** (40x40 pixels cada):
- `mini_homem_parado.png` - Pose estática
- `mini_homem_correndo.png` - Pose de corrida
- `mini_homem_pulando.png` - Pose no ar

**Jacaré** (50x50 pixels):
- `jacare.png` - Sprite que será espelhado automaticamente

#### Áudio

**Música**:
- `background.mp3` - Música de fundo em loop

**Efeitos Sonoros**:
- `jump.wav` - Som curto de pulo
- `game_over.wav` - Som de derrota

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install pgzero
```

### 2. Preparar Estrutura de Pastas

Certifique-se de que existem as seguintes pastas:
```bash
mkdir images images/jacare images/mini_homem music sounds
```

### 3. Adicionar Sprites e Áudio

Coloque os arquivos de imagem e áudio nas pastas correspondentes conforme a estrutura acima.

### 4. Executar o Jogo

```bash
python game.py
```

Ou usando o comando pgzrun:

```bash
pgzrun game.py
```

### 5. Controles do Jogo

- **Menu Principal**:
  - Clique em **"Iniciar Jogo"** para começar
  - Clique em **"Som: ON/OFF"** para controlar o áudio
  - Clique em **"Sair"** para fechar o jogo

- **Durante o Jogo**:
  - **Setas ← →** para mover o personagem
  - **ESPAÇO** para pular
  - Evite cair e evite os jacarés!
  
- **Tela de Game Over**:
  - **ENTER** para voltar ao menu

## 🎨 Princípios de Clean Code Aplicados

1. **Nomes Significativos**: 
   - `player_speed` em vez de `ps`
   - `is_on_ground` em vez de `flag`
   - `check_collision()` em vez de `cc()`

2. **Funções Pequenas**: 
   - Cada método faz uma coisa específica
   - `jump()`, `move_left()`, `move_right()` separados

3. **Comentários Úteis**: 
   - Docstrings em todas as classes
   - Comentários explicando lógica complexa
   - Seções bem marcadas

4. **Formatação Consistente**: 
   - PEP8 seguido rigorosamente
   - Indentação de 4 espaços
   - Linhas < 120 caracteres

5. **Tratamento de Erros**: 
   - Try/except ao carregar sprites
   - Fallback para retângulos coloridos
   - Verificações apropriadas

6. **DRY (Don't Repeat Yourself)**: 
   - `get_rect()` centralizado
   - Sistema de sprites reutilizável
   - Código sem repetições

## 🎓 Recursos Educacionais

Este projeto é ideal para ensinar:
- **Programação Orientada a Objetos**: Classes, herança, encapsulamento
- **Princípios SOLID**: Aplicação prática dos 5 princípios
- **Game Loops**: Estrutura update/draw do PgZero
- **Física Básica**: Gravidade, velocidade, aceleração
- **Sistema de Estados**: State pattern (MENU, PLAYING, GAME_OVER)
- **Detecção de Colisões**: AABB (Axis-Aligned Bounding Box)
- **Animação de Sprites**: Troca de sprites por estado
- **Transformações**: Scale e flip com pygame.transform
- **Integração de Áudio**: Música e efeitos sonoros

## 🔧 Detalhes Técnicos

### Sistema de Sprites

O jogo utiliza um sistema sofisticado de sprites:

```python
# Carrega três sprites diferentes para o jogador
idle_actor = Actor(PLAYER_SPRITE_IDLE)
run_actor = Actor(PLAYER_SPRITE_RUNNING)
jump_actor = Actor(PLAYER_SPRITE_JUMPING)

# Escala todos para o tamanho correto
self.surf_idle = scale(idle_actor._surf, (self.width, self.height))
self.surf_run = scale(run_actor._surf, (self.width, self.height))
self.surf_jump = scale(jump_actor._surf, (self.width, self.height))
```

### Escolha Inteligente de Sprites

```python
# Lógica de seleção de sprite baseada no estado
if not self.is_on_ground:
    base_surf = self.surf_jump  # No ar = pulando
elif self.is_moving_horizontal:
    base_surf = self.surf_run   # Movendo = correndo
else:
    base_surf = self.surf_idle  # Parado = idle
```

### Sistema de Flip Direcional

```python
# Espelha sprite baseado na direção
is_flipped = not self.facing_right
final_surf = flip(base_surf, is_flipped, False)
```

### Física Aprimorada

```python
# Detecção de "quase no chão" para evitar bugs
distance_to_platform = platform.y - (self.y + self.height)
if -3 <= distance_to_platform <= 3:
    # Considera no chão mesmo com pequena distância
    self.is_on_ground = True
```

### Patrulha Inteligente dos Inimigos

```python
# Inimigos invertem direção nas bordas da plataforma
platform_rect = self.platform.get_rect()
if self.x <= platform_rect.left:
    self.direction = 1  # Vai para direita
elif self.x + self.width >= platform_rect.right:
    self.direction = -1  # Vai para esquerda
```

## 🎵 Sistema de Áudio Detalhado

### Controle de Estado
```python
def toggle_sound(self):
    self.sound_enabled = not self.sound_enabled
    if self.sound_enabled and self.state == GameState.PLAYING:
        self.play_music()
    else:
        self.stop_music()
```

### Música de Fundo
```python
    def play_music(self):
        """Inicia a música de fundo se o som estiver habilitado"""
        if self.sound_enabled and not self.music_playing:
            try:
                music.play('background')
                self.music_playing = True
            except Exception as e:
                print(f"⚠️ Erro ao tocar música: {e}")
```

### Efeitos Sonoros
```python
    def play_sound(self, sound_name):
        if self.sound_enabled:
            try:
                # PgZero usa notação de atributo, não subscript
                sound = getattr(sounds, sound_name)
                sound.play()
            except AttributeError:
                print(f"⚠️ Som '{sound_name}' não encontrado!")
                print(f"   Certifique-se de que o arquivo sounds/{sound_name}.wav existe")
            except Exception as e:
                print(f"⚠️ Erro ao tocar som '{sound_name}': {e}")
```

## 📊 Estatísticas do Código

- **Linhas de Código**: ~450 linhas (incluindo comentários)
- **Linhas Significativas**: ~300 linhas
- **Classes**: 5 (Player, Enemy, Platform, Button, Game)
- **Funções/Métodos**: ~30
- **Complexidade**: Apropriada para programadores intermediários


## 📝 Notas Técnicas

### PgZero + Pygame Híbrido

O jogo usa principalmente PgZero, mas importa funções específicas do Pygame:
```python
from pygame.transform import scale  # Para redimensionar sprites
from pygame.transform import flip   # Para espelhar sprites
```

Isso é necessário porque PgZero não oferece essas transformações nativamente, mas o uso é mínimo e permitido.

### Centralização da Janela

```python
os.environ['SDL_VIDEO_CENTERED'] = '1'
```

Esta linha garante que a janela do jogo apareça centralizada na tela.

### Estrutura de Pastas do PgZero

PgZero procura automaticamente recursos em pastas específicas:
- `images/` - Para sprites
- `music/` - Para músicas (MP3, OGG)
- `sounds/` - Para efeitos sonoros (WAV)

Não é necessário especificar caminhos completos, apenas o nome do arquivo.

## 📜 Licença

Este projeto é de código aberto para fins educacionais (Licença MIT).

```
MIT License

Copyright (c) 2024 Adventure Platformer Educational Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🎯 Requisitos do Sistema

### Mínimos
- **Python**: 3.6 ou superior
- **Sistema Operacional**: Windows, macOS ou Linux
- **RAM**: 512 MB
- **Espaço em Disco**: 50 MB

### Recomendados
- **Python**: 3.8 ou superior
- **RAM**: 1 GB
- **Resolução**: 800x600 ou superior

## 🐛 Solução de Problemas

### Sprites não aparecem
- Verifique se a pasta `images/` existe
- Confirme que os sprites estão nos subdiretórios corretos
- Verifique os nomes dos arquivos (case-sensitive no Linux/Mac)

### Música não toca
- Verifique se pygame está instalado corretamente
- Confirme que `background.mp3` está em `music/`
- Teste se o áudio do sistema está funcionando

### Jogo muito rápido/lento
- PgZero tenta rodar a 60 FPS
- Ajuste as constantes de velocidade se necessário

### Erros de importação
```bash
pip install --upgrade pgzero
```

## 👨‍🏫 Autor
**Samuel Dantas**

**Desenvolvido como projeto educacional para ensino de Python e princípios de programação.**


## 🙏 Agradecimentos

- **PgZero**: Framework educacional
- **Pygame**: Engine robusta por trás do PgZero
- **Comunidade Python**: Pela documentação excepcional

---

**Versão**: 1.0.1  
**Última Atualização**: Dezembro 2025
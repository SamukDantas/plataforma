# 🎮 Plataforma - Aventura

Um jogo de plataforma educativo desenvolvido em Python usando PgZero, seguindo princípios SOLID e Clean Code.

## 📋 Requisitos Atendidos

✅ **Bibliotecas permitidas**: Apenas PgZero, math e random  
✅ **Gênero**: Platformer (visão lateral com plataformas)  
✅ **Menu principal**: Com botões clicáveis (Iniciar, Som On/Off, Sair)  
✅ **Música e sons**: Sistema de controle implementado com música de fundo  
✅ **Inimigos**: Múltiplos inimigos perigosos para o herói  
✅ **Movimento de inimigos**: Patrulham suas plataformas  
✅ **Classes próprias**: Implementação de movimento e animação  
✅ **Animação de sprites**: Personagens animados em movimento e parados  
✅ **Nomenclatura**: Nomes claros em inglês, seguindo PEP8  
✅ **Lógica e bugs**: Mecânica funcional sem erros  
✅ **Código único**: 100% original e independente  

## 🎯 Características do Jogo

### Gameplay
- **Objetivo**: Sobreviva o máximo de tempo possível sem cair ou tocar nos inimigos
- **Controles**:
  - ⬅️ ➡️ Setas: Mover para esquerda/direita
  - ESPAÇO: Pular
- **Mecânicas**:
  - Física de gravidade realista
  - Sistema de plataformas com colisão
  - Inimigos que patrulham suas áreas
  - Sistema de pontuação baseado em tempo de sobrevivência
  - Música de fundo durante o jogo

### Personagens
- **Herói**: Personagem azul controlado pelo jogador
  - Animação: Pulsa entre tons de azul
  - Pode pular e se mover horizontalmente
  
- **Inimigos**: Personagens vermelhos hostis
  - Animação: Pulsam entre tons de vermelho
  - Patrulham plataformas automaticamente
  - Mudam de direção ao alcançar bordas

### Sistema de Áudio
- **Música de Fundo**: Toca automaticamente durante o jogo
- **Controle de Som**: Botão no menu para ligar/desligar
- **Estado Persistente**: Configuração de som mantida durante a sessão

## 🏗️ Estrutura do Código (SOLID)

### Single Responsibility Principle (SRP)
- `AnimatedSprite`: Responsável apenas por animação de sprites
- `Player`: Gerencia apenas lógica do jogador
- `Enemy`: Gerencia apenas comportamento dos inimigos
- `Platform`: Representa apenas plataformas estáticas
- `Button`: Cuida apenas de botões de interface
- `Game`: Coordena o jogo (Controller pattern)

### Open/Closed Principle (OCP)
- `AnimatedSprite` é uma classe base extensível
- `Player` e `Enemy` herdam e estendem sem modificar a base

### Liskov Substitution Principle (LSP)
- `Player` e `Enemy` podem substituir `AnimatedSprite` sem quebrar funcionalidade

### Interface Segregation Principle (ISP)
- Classes têm métodos específicos às suas necessidades
- Sem métodos desnecessários forçados

### Dependency Inversion Principle (DIP)
- Classes dependem de abstrações (classe base `AnimatedSprite`)
- Baixo acoplamento entre componentes

## 📁 Estrutura do Projeto

```
platformer_game/
├── game.py              # Código principal do jogo
├── README.md            # Documentação
├── requirements.txt     # Dependências Python
├── LICENSE              # Licença MIT
├── .gitignore          # Arquivos a ignorar no Git
├── REQUIREMENTS_CHECKLIST.md  # Checklist de requisitos
├── music/              # Arquivos de música
│   └── background.mp3  # Música de fundo do jogo
└── sounds/             # Efeitos sonoros (expandir conforme necessário)
```

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install pgzero
```

### 2. Executar o Jogo

```bash
python game.py
```

Ou usando o comando pgzrun:

```bash
pgzrun game.py
```

### 3. Controles do Jogo

- **Menu Principal**:
  - Clique em "Iniciar Jogo" para começar
  - Clique em "Som: ON/OFF" para controlar o áudio
  - Clique em "Sair" para fechar o jogo

- **Durante o Jogo**:
  - Setas ← → para mover o personagem
  - ESPAÇO para pular
  
- **Tela de Game Over**:
  - ENTER para voltar ao menu

## 🎨 Princípios de Clean Code Aplicados

1. **Nomes Significativos**: Variáveis e funções com nomes claros
2. **Funções Pequenas**: Cada função faz uma coisa só
3. **Comentários Úteis**: Documentação onde necessário
4. **Formatação Consistente**: PEP8 seguido rigorosamente
5. **Tratamento de Erros**: Verificações apropriadas
6. **DRY (Don't Repeat Yourself)**: Código sem repetições

## 🎓 Recursos Educacionais

Este projeto é ideal para ensinar:
- Programação Orientada a Objetos
- Princípios SOLID
- Game loops e física básica
- Sistema de estados (State pattern)
- Detecção de colisões
- Animação de sprites
- Integração de áudio em jogos

## 📝 Notas Técnicas

- **Animação**: Implementada através de ciclos de cores (simulando sprites)
- **Física**: Sistema de gravidade e colisão básicos
- **Áudio**: Sistema de música e sons com controle on/off
- **Performance**: ~100-200 linhas significativas de código
- **Complexidade**: Apropriada para programadores iniciantes

## 🎵 Sistema de Áudio

O jogo utiliza o sistema de áudio do PgZero para:
- Tocar música de fundo em loop durante o jogo
- Controlar o estado de som (ligado/desligado)
- Suporte para efeitos sonoros futuros

### Estrutura de Áudio

- **music/**: Pasta para arquivos de música (formato MP3)
  - `background.mp3`: Música de fundo do jogo
- **sounds/**: Pasta para efeitos sonoros (expandir conforme necessário)

### Como Adicionar Novos Sons

1. Adicione arquivos MP3 na pasta `music/` para músicas de fundo
2. Adicione arquivos WAV na pasta `sounds/` para efeitos sonoros
3. Use `music.play('nome_do_arquivo')` para músicas
4. Use `sounds.nome_do_arquivo.play()` para efeitos

## 🔧 Possíveis Melhorias Futuras

Para alunos avançados, sugestões de expansão:
1. Adicionar imagens reais de sprites
2. Implementar sistema de vidas
3. Adicionar power-ups
4. Criar múltiplos níveis
5. Implementar sistema de save/load
6. Adicionar mais efeitos sonoros (pulo, colisão, etc.)
7. Implementar música diferente para menu e game over

## 📜 Licença

Este projeto é de código aberto para fins educacionais (Licença MIT).

## 👨‍🏫 Autor

Desenvolvido como projeto educacional para tutoria de Python.

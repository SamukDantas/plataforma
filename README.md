# 🎮 Plataforma - aventura

Um jogo de plataforma educativo desenvolvido em Python usando PgZero, seguindo princípios SOLID e Clean Code.

## 📋 Requisitos Atendidos

✅ **Bibliotecas permitidas**: Apenas PgZero, math e random  
✅ **Gênero**: Platformer (visão lateral com plataformas)  
✅ **Menu principal**: Com botões clicáveis (Iniciar, Som On/Off, Sair)  
✅ **Música e sons**: Sistema de controle implementado  
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

### Personagens
- **Herói**: Personagem azul controlado pelo jogador
  - Animação: Pulsa entre tons de azul
  - Pode pular e se mover horizontalmente
  
- **Inimigos**: Personagens vermelhos hostis
  - Animação: Pulsam entre tons de vermelho
  - Patrulham plataformas automaticamente
  - Mudam de direção ao alcançar bordas

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
└── .gitignore          # Arquivos a ignorar no Git
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

## 📝 Notas Técnicas

- **Animação**: Implementada através de ciclos de cores (simulando sprites)
- **Física**: Sistema de gravidade e colisão básicos
- **Performance**: ~100-200 linhas significativas de código
- **Complexidade**: Apropriada para programadores iniciantes

## 🔧 Possíveis Melhorias Futuras

Para alunos avançados, sugestões de expansão:
1. Adicionar imagens reais de sprites
2. Implementar sistema de vidas
3. Adicionar power-ups
4. Criar múltiplos níveis
5. Implementar sistema de save/load
6. Adicionar efeitos sonoros reais

## 📜 Licença

Este projeto é de código aberto para fins educacionais.

## 👨‍🏫 Autor

Desenvolvido como projeto educacional para tutoria de Python.

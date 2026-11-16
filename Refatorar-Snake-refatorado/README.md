# Refatorar-Snake

Projeto refatorado para a disciplina **Manutenção de Software** (Refatoração Segura com Testes Automatizados e Mapeamento de Classes em Python).

## Mapeamento de Classes e Estrutura do Projeto

O código monolítico original (`Snake.py`) foi reorganizado em módulos coesos dentro de `src/` aplicando separação de responsabilidades (MVC/Camadas):

- **`src/config.py`**: Centraliza constantes de tela, grade, FPS, direções e paleta de cores (eliminando *Magic Numbers*).
- **`src/entities.py`**:
  - `Apple`: Gerencia a posição e reposicionamento da maçã na grade.
  - `Snake`: Representa a cobra base, encapsulando movimentação, crescimento e detecção de colisões.
  - `AISnake`: Herda de `Snake` e implementa a lógica de perseguição da maçã e desvio de obstáculos.
- **`src/game_logic.py`**:
  - `GameState`: Controla o estado da partida, pontuação, vidas bônus, transição de fases (1 a 4), alternância de cores e resolução de colisões.
- **`src/renderer.py`**:
  - `GameRenderer`: Isola toda a renderização gráfica com Pygame (cenários, grade, HUD e telas de vitória/game over).
- **`src/main.py` e `Snake.py`**: Gerenciam o loop principal e a captura de eventos de entrada.
- **`tests/`**: Suíte de testes automatizados com `pytest` cobrindo mais de 80% do código em `src/`.

## Como Executar

### Executar o Jogo
```bash
pip install -r requirements.txt
python Snake.py
```

### Executar os Testes Automatizados com Cobertura
```bash
pytest --cov=src --cov-fail-under=80
```

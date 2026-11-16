"""Entidades do jogo Snake: grid, maçã, cobra do jogador e cobra controlada por IA."""

import random
from typing import Callable, List, Tuple
from src.config import (
    DOWN,
    GRID_COLUMNS,
    GRID_ROWS,
    GRID_SIZE,
    LEFT,
    RIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UP,
)

Position = Tuple[int, int]


def on_grid_random(rng: random.Random | None = None) -> Position:
    """Gera uma posição aleatória alinhada à grade."""
    generator = rng if rng is not None else random
    x = generator.randint(0, GRID_COLUMNS - 1)
    y = generator.randint(0, GRID_ROWS - 1)
    return (x * GRID_SIZE, y * GRID_SIZE)


def check_collision(c1: Position, c2: Position) -> bool:
    """Verifica se duas posições ocupam a mesma célula da grade."""
    return c1[0] == c2[0] and c1[1] == c2[1]


class Apple:
    """Representa a maçã coletável no tabuleiro."""

    def __init__(self, position: Position | None = None, rng: random.Random | None = None):
        self._rng = rng
        self.position: Position = position if position is not None else on_grid_random(self._rng)

    def respawn(self) -> Position:
        """Reposiciona a maçã aleatoriamente na grade."""
        self.position = on_grid_random(self._rng)
        return self.position


class Snake:
    """Representa uma cobra no jogo (jogador ou base para IA)."""

    def __init__(
        self,
        initial_body: List[Position] | None = None,
        direction: int = LEFT,
    ):
        self.body: List[Position] = (
            list(initial_body)
            if initial_body is not None
            else [(200, 200), (210, 200), (220, 200)]
        )
        self.direction: int = direction

    @property
    def head(self) -> Position:
        """Retorna a posição da cabeça da cobra."""
        return self.body[0]

    def set_direction(self, new_direction: int) -> None:
        """Altera a direção impedindo inversão direta de 180 graus."""
        opposites = {
            UP: DOWN,
            DOWN: UP,
            LEFT: RIGHT,
            RIGHT: LEFT,
        }
        if new_direction in opposites and opposites[new_direction] != self.direction:
            self.direction = new_direction

    def grow(self) -> None:
        """Adiciona um novo segmento à cauda da cobra."""
        self.body.append((0, 0))

    def move_body_segments(self) -> None:
        """Desloca cada segmento do corpo para a posição do segmento anterior."""
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])

    def compute_next_head(self) -> Position:
        """Calcula a próxima coordenada da cabeça com base na direção atual."""
        x, y = self.head
        if self.direction == UP:
            return (x, y - GRID_SIZE)
        if self.direction == DOWN:
            return (x, y + GRID_SIZE)
        if self.direction == RIGHT:
            return (x + GRID_SIZE, y)
        if self.direction == LEFT:
            return (x - GRID_SIZE, y)
        return (x, y)

    def move(self) -> None:
        """Avança o corpo e a cabeça da cobra em uma unidade da grade."""
        self.move_body_segments()
        self.body[0] = self.compute_next_head()

    def is_out_of_bounds(self) -> bool:
        """Verifica se a cabeça ultrapassou os limites da tela."""
        x, y = self.head
        return x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT or x < 0 or y < 0

    def collides_with_self(self) -> bool:
        """Verifica se a cabeça colidiu com algum segmento do próprio corpo."""
        return any(self.head == segment for segment in self.body[1:])

    def collides_with_other(self, other: "Snake") -> bool:
        """Verifica se a cabeça colidiu com o corpo de outra cobra."""
        if len(other.body) <= 2:
            return False
        return any(self.head == segment for segment in other.body[1:-1])


class AISnake(Snake):
    """Cobra controlada por inteligência artificial simples que persegue a maçã."""

    def __init__(
        self,
        initial_body: List[Position] | None = None,
        direction: int = LEFT,
        rng: random.Random | None = None,
    ):
        body = initial_body if initial_body is not None else [(100, 100), (110, 100), (120, 100)]
        super().__init__(initial_body=body, direction=direction)
        self.should_move: bool = True
        self._rng = rng

    def decide_direction(self, apple_pos: Position) -> None:
        """Define a direção em direção à posição da maçã."""
        head_x, head_y = self.head
        apple_x, apple_y = apple_pos

        if apple_x > head_x and self.direction != LEFT:
            self.direction = RIGHT
        if apple_x < head_x and self.direction != RIGHT:
            self.direction = LEFT
        if apple_y > head_y and self.direction != UP:
            self.direction = DOWN
        if apple_y < head_y and self.direction != DOWN:
            self.direction = UP

    def update_position(
        self,
        player_body: List[Position],
        random_pos_fn: Callable[[], Position] | None = None,
    ) -> None:
        """Atualiza a cabeça da cobra IA evitando obstáculos ou reposicionando aleatoriamente."""
        if not self.should_move:
            return

        next_pos = self.compute_next_head()
        out_of_bounds = (
            next_pos[0] < 0
            or next_pos[1] < 0
            or next_pos[0] > SCREEN_WIDTH - GRID_SIZE
            or next_pos[1] > SCREEN_HEIGHT - GRID_SIZE
        )

        if next_pos in self.body or next_pos in player_body or out_of_bounds:
            pos_generator = random_pos_fn if random_pos_fn is not None else lambda: on_grid_random(self._rng)
            self.body[0] = pos_generator()
        else:
            self.body[0] = next_pos
            self.should_move = True

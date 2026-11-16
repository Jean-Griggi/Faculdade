"""Regras de negócio, progressão de fases e estado do jogo Snake."""

import random
from src.config import (
    COLOR_AI_ALT_1,
    COLOR_AI_ALT_2,
    COLOR_AI_FASE_3,
    COLOR_MAGENTA,
    COLOR_PLAYER_FASE_3,
    COLOR_YELLOW,
)
from src.entities import AISnake, Apple, Snake, check_collision


class GameState:
    """Gerencia o estado, pontuação, vidas, fases e colisões do jogo."""

    def __init__(self, rng: random.Random | None = None):
        self.rng = rng
        self.player = Snake()
        self.ai_snake = AISnake(rng=self.rng)
        self.apple = Apple(rng=self.rng)

        self.score: int = 0
        self.score_ai: int = 0
        self.fase: int = 1
        self.vida: int = 3
        self.game_over: bool = False
        self.victory: bool = False

        self.player_color: tuple[int, int, int] = COLOR_YELLOW
        self.ai_color: tuple[int, int, int] = COLOR_MAGENTA
        self._ai_color_toggle: int = 1
        self._player_color_toggle: int = 1

    def update_phase_and_bonus_lives(self) -> None:
        """Atualiza a fase atual e concede vidas extras conforme a pontuação."""
        if self.score < 30:
            self.fase = 1
        if self.score >= 30:
            self.fase = 2
        if self.score == 40:
            self.vida += 1
        if self.score >= 50:
            self.fase = 3
        if self.score == 50:
            self.vida += 1
        if self.score == 65:
            self.fase = 4
            self.victory = True

    def _toggle_ai_color_standard(self) -> None:
        """Alterna a cor da cobra IA nas fases 1 e 2."""
        if self._ai_color_toggle == 0:
            self.ai_color = COLOR_AI_ALT_1
            self._ai_color_toggle = 1
        else:
            self.ai_color = COLOR_AI_ALT_2
            self._ai_color_toggle = 0

    def _toggle_colors_phase_3(self) -> None:
        """Alterna as cores das cobras na fase 3."""
        if self._player_color_toggle == 0:
            self.player_color = COLOR_PLAYER_FASE_3
            self._player_color_toggle = 1
        else:
            self.ai_color = COLOR_AI_FASE_3
            self._ai_color_toggle = 0

    def step(self) -> None:
        """Executa um ciclo completo de atualização lógica do jogo."""
        if self.game_over or self.victory:
            return

        self.update_phase_and_bonus_lives()

        if self.fase == 4:
            self.victory = True
            return

        # Coleta da maçã pelo jogador
        if check_collision(self.player.head, self.apple.position):
            self.apple.respawn()
            self.player.grow()
            self.score += 1

        # Movimento do jogador
        self.player.move()

        # Movimento da cobra IA
        self.ai_snake.decide_direction(self.apple.position)
        self.ai_snake.update_position(self.player.body)
        self.ai_snake.move_body_segments()

        # Coleta da maçã pela cobra IA
        if check_collision(self.ai_snake.head, self.apple.position):
            self.apple.respawn()
            self.ai_snake.grow()
            if self.fase in (1, 2):
                self.score_ai += 1
            elif self.fase == 3:
                self.score -= 1

        # Atualização visual das cores
        if self.fase in (1, 2):
            self._toggle_ai_color_standard()
        elif self.fase == 3:
            self._toggle_colors_phase_3()

        # Verificação de colisões
        self._resolve_collisions()

    def _resolve_collisions(self) -> None:
        """Avalia colisões com bordas, corpo da IA e próprio corpo."""
        if self.player.is_out_of_bounds():
            self.vida = -1

        if self.vida < 0:
            self.game_over = True
            return

        if self.player.collides_with_other(self.ai_snake):
            if self.fase in (1, 2):
                self.vida -= 1
            elif self.fase == 3:
                self.vida += 1
                self.score_ai -= 1

        if self.player.collides_with_self():
            self.vida -= 1

        if self.vida < 0:
            self.game_over = True

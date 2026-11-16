"""Testes unitários para o fluxo de estados, fases, pontuação e colisões."""

import random
from src.config import (
    COLOR_AI_ALT_1,
    COLOR_AI_ALT_2,
    COLOR_AI_FASE_3,
    COLOR_PLAYER_FASE_3,
    LEFT,
)
from src.game_logic import GameState


def test_initial_game_state():
    state = GameState(rng=random.Random(1))
    assert state.score == 0
    assert state.score_ai == 0
    assert state.fase == 1
    assert state.vida == 3
    assert state.game_over is False
    assert state.victory is False


def test_phase_transitions_and_bonus_lives():
    state = GameState(rng=random.Random(1))

    state.score = 29
    state.update_phase_and_bonus_lives()
    assert state.fase == 1

    state.score = 30
    state.update_phase_and_bonus_lives()
    assert state.fase == 2

    state.score = 40
    state.update_phase_and_bonus_lives()
    assert state.vida == 4

    state.score = 50
    state.update_phase_and_bonus_lives()
    assert state.fase == 3
    assert state.vida == 5

    state.score = 65
    state.update_phase_and_bonus_lives()
    assert state.fase == 4
    assert state.victory is True


def test_player_eats_apple_and_ai_color_toggles():
    state = GameState(rng=random.Random(2))
    state.player.body = [(200, 200), (210, 200), (220, 200)]
    state.player.direction = LEFT
    state.apple.position = (200, 200)

    state.step()
    assert state.score == 1
    assert len(state.player.body) == 4
    assert state.ai_color == COLOR_AI_ALT_2

    state.step()
    assert state.ai_color == COLOR_AI_ALT_1


def test_ai_eats_apple_in_phase_1_and_phase_3():
    state = GameState(rng=random.Random(3))
    # Posicionar IA para cair em cima da maçã após update_position
    state.ai_snake.body = [(110, 100), (120, 100), (130, 100)]
    state.ai_snake.direction = LEFT
    state.apple.position = (100, 100)

    state.step()
    assert state.score_ai == 1
    assert len(state.ai_snake.body) == 4

    # Testar fase 3 (IA rouba pontos do jogador e alterna cores)
    state.score = 52
    state.ai_snake.body = [(110, 100), (120, 100), (130, 100)]
    state.ai_snake.direction = LEFT
    state.apple.position = (100, 100)
    state.step()
    assert state.fase == 3
    assert state.score == 51
    assert state.ai_color == COLOR_AI_FASE_3

    state._player_color_toggle = 0
    state.step()
    assert state.player_color == COLOR_PLAYER_FASE_3


def test_collisions_with_ai_and_self_and_walls():
    state = GameState(rng=random.Random(4))
    # Colisão jogador com corpo da IA na fase 1 reduz vida
    state.player.body = [(120, 100), (130, 100), (140, 100)]
    state.player.direction = LEFT
    state.ai_snake.body = [(100, 100), (110, 100), (120, 100), (130, 100)]
    state.ai_snake.should_move = False
    state.step()
    assert state.vida == 2

    # Colisão jogador com corpo da IA na fase 3 dá vida e tira ponto do chefão
    state.score = 55
    state.score_ai = 5
    state.player.body = [(120, 100), (130, 100), (140, 100)]
    state.player.direction = LEFT
    state.ai_snake.body = [(100, 100), (110, 100), (120, 100), (130, 100)]
    state.step()
    assert state.vida == 3
    assert state.score_ai == 4

    # Colisão com o próprio corpo reduz vida
    state.player.body = [(110, 100), (110, 110), (100, 110), (100, 100), (100, 90)]
    state.player.direction = LEFT
    state.step()
    assert state.vida == 2

    # Colisão com a parede resulta em Game Over imediato
    state.player.body = [(0, 100), (10, 100), (20, 100)]
    state.player.direction = LEFT
    state.step()
    assert state.vida == -1
    assert state.game_over is True

    # Após game_over, step não executa mais alterações
    prev_score = state.score
    state.step()
    assert state.score == prev_score


def test_step_reaches_victory_on_phase_4():
    state = GameState(rng=random.Random(5))
    state.score = 65
    state.step()
    assert state.fase == 4
    assert state.victory is True

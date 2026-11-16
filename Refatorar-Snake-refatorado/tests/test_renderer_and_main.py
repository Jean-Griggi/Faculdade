"""Testes automatizados para renderização (com Pygame headless) e entrada."""

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from pygame.locals import K_a, K_d, K_s, K_w, KEYDOWN, QUIT
from src.config import DOWN, LEFT, RIGHT, UP
from src.game_logic import GameState
from src.main import handle_input
from src.renderer import GameRenderer


def test_renderer_frames_and_game_over():
    pygame.init()
    try:
        renderer = GameRenderer(base_assets_dir=".")
        state = GameState()

        # Fase 1 (com grade)
        state.fase = 1
        renderer.render_frame(state)

        # Fase 2
        state.fase = 2
        renderer.render_frame(state)

        # Fase 3 (com pontuação do chefão)
        state.fase = 3
        renderer.render_frame(state)

        # Vitória
        state.victory = True
        renderer.render_frame(state)

        # Game Over
        renderer.render_game_over()
    finally:
        pygame.quit()


def test_handle_input_events():
    pygame.init()
    try:
        state = GameState()
        state.player.direction = LEFT

        # Direção para cima (W)
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_w))
        assert handle_input(state) is True
        assert state.player.direction == UP

        # Direção para direita (D)
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_d))
        assert handle_input(state) is True
        assert state.player.direction == RIGHT

        # Direção para baixo (S)
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_s))
        assert handle_input(state) is True
        assert state.player.direction == DOWN

        # Direção para esquerda (A)
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_a))
        assert handle_input(state) is True
        assert state.player.direction == LEFT

        # Evento QUIT
        pygame.event.post(pygame.event.Event(QUIT))
        assert handle_input(state) is False
    finally:
        pygame.quit()

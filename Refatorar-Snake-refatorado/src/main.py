"""Ponto de entrada principal para execução do jogo Snake."""

import sys
import time
import pygame
from pygame.locals import K_a, K_d, K_s, K_w, KEYDOWN, QUIT
from src.config import DOWN, FPS, LEFT, RIGHT, UP
from src.game_logic import GameState
from src.renderer import GameRenderer


def handle_input(state: GameState) -> bool:
    """Processa eventos de teclado e janela. Retorna False se o usuário fechar o jogo."""
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        if event.type == KEYDOWN:
            if event.key == K_w:
                state.player.set_direction(UP)
            elif event.key == K_s:
                state.player.set_direction(DOWN)
            elif event.key == K_a:
                state.player.set_direction(LEFT)
            elif event.key == K_d:
                state.player.set_direction(RIGHT)
    return True


def run_game() -> None:
    """Inicializa o Pygame e executa o loop principal do jogo."""
    pygame.init()
    clock = pygame.time.Clock()
    state = GameState()
    renderer = GameRenderer()

    while not state.game_over and not state.victory:
        clock.tick(FPS)
        if not handle_input(state):
            pygame.quit()
            sys.exit()

        state.step()
        renderer.render_frame(state)

        if state.victory:
            time.sleep(7)
            break

    renderer.render_game_over()
    pygame.time.wait(500)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    run_game()

"""Camada de renderização gráfica utilizando Pygame."""

import os
import pygame
from src.config import (
    COLOR_BLACK,
    COLOR_BOSS_SCORE,
    COLOR_FASE_1_2,
    COLOR_FASE_3,
    COLOR_GRID,
    COLOR_SCORE,
    COLOR_VIDA_1,
    COLOR_VIDA_2_3,
    COLOR_WHITE,
    COLOR_WIN_TEXT,
    GRID_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from src.game_logic import GameState


class GameRenderer:
    """Responsável por carregar recursos visuais e desenhar cada frame do jogo."""

    def __init__(self, base_assets_dir: str = "."):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")

        self.backgrounds = {
            1: self._load_background(os.path.join(base_assets_dir, "FUNDO.jpeg")),
            2: self._load_background(os.path.join(base_assets_dir, "FUNDO2.jpg")),
            3: self._load_background(os.path.join(base_assets_dir, "FUNDO3.jpg")),
        }

        self.snake_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.ai_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.apple_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.apple_surface.fill(COLOR_WHITE)

        self.hud_font = pygame.font.Font("freesansbold.ttf", 18)
        self.win_font = pygame.font.Font("freesansbold.ttf", 50)
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 75)

    @staticmethod
    def _load_background(path: str) -> pygame.Surface:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw_grid(self) -> None:
        """Desenha as linhas da grade na fase 1."""
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

    def draw_hud(self, state: GameState) -> None:
        """Desenha pontuação, fase, vidas e pontuação do chefão na tela."""
        score_surf = self.hud_font.render(f"Score: {state.score}", True, COLOR_SCORE)
        score_rect = score_surf.get_rect(topleft=(SCREEN_WIDTH - 120, 10))
        self.screen.blit(score_surf, score_rect)

        fase_color = COLOR_FASE_3 if state.fase == 3 else COLOR_FASE_1_2
        fase_surf = self.hud_font.render(f"Fase: {state.fase}", True, fase_color)
        fase_rect = fase_surf.get_rect(topleft=(SCREEN_WIDTH - 200, 10))
        self.screen.blit(fase_surf, fase_rect)

        vida_color = COLOR_VIDA_1 if state.fase == 1 else COLOR_VIDA_2_3
        vida_surf = self.hud_font.render(f"Vida: {state.vida}", True, vida_color)
        vida_rect = vida_surf.get_rect(topleft=(0, 10))
        self.screen.blit(vida_surf, vida_rect)

        if state.fase == 3:
            boss_surf = self.hud_font.render(f"Chefão: {state.score_ai}", True, COLOR_BOSS_SCORE)
            boss_rect = boss_surf.get_rect(topleft=(SCREEN_WIDTH - 350, 10))
            self.screen.blit(boss_surf, boss_rect)

    def render_frame(self, state: GameState) -> None:
        """Renderiza o estado atual do jogo."""
        if state.victory:
            win_surf = self.win_font.render("Você Venceu!!!", True, COLOR_WIN_TEXT)
            win_rect = win_surf.get_rect(midtop=(SCREEN_WIDTH / 2, 10))
            self.screen.blit(win_surf, win_rect)
            pygame.display.update()
            return

        bg = self.backgrounds.get(state.fase, self.backgrounds[1])
        self.screen.blit(bg, (0, 0))
        self.screen.blit(self.apple_surface, state.apple.position)

        if state.fase == 1:
            self.draw_grid()

        self.draw_hud(state)

        self.snake_surface.fill(state.player_color)
        for pos in state.player.body:
            self.screen.blit(self.snake_surface, pos)

        self.ai_surface.fill(state.ai_color)
        for pos in state.ai_snake.body:
            self.screen.blit(self.ai_surface, pos)

        pygame.display.update()

    def render_game_over(self) -> None:
        """Renderiza a tela de fim de jogo."""
        over_surf = self.game_over_font.render("Game Over", True, COLOR_BLACK)
        over_rect = over_surf.get_rect(midtop=(SCREEN_WIDTH / 2, 10))
        self.screen.blit(over_surf, over_rect)
        pygame.display.update()

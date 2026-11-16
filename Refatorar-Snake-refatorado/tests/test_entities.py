"""Testes unitários para entidades e funções geométricas."""

import random
from src.config import DOWN, GRID_SIZE, LEFT, RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, UP
from src.entities import AISnake, Apple, Snake, check_collision, on_grid_random


def test_on_grid_random_alignment():
    rng = random.Random(42)
    for _ in range(50):
        x, y = on_grid_random(rng)
        assert 0 <= x < SCREEN_WIDTH
        assert 0 <= y < SCREEN_HEIGHT
        assert x % GRID_SIZE == 0
        assert y % GRID_SIZE == 0


def test_check_collision():
    assert check_collision((100, 100), (100, 100)) is True
    assert check_collision((100, 100), (110, 100)) is False
    assert check_collision((100, 100), (100, 110)) is False


def test_apple_creation_and_respawn():
    rng = random.Random(10)
    apple = Apple(position=(50, 50), rng=rng)
    assert apple.position == (50, 50)
    new_pos = apple.respawn()
    assert new_pos == apple.position
    assert new_pos[0] % GRID_SIZE == 0


def test_snake_movement_all_directions():
    snake = Snake(initial_body=[(100, 100), (110, 100), (120, 100)], direction=LEFT)
    snake.move()
    assert snake.body == [(90, 100), (100, 100), (110, 100)]

    snake.set_direction(UP)
    snake.move()
    assert snake.head == (90, 90)

    snake.set_direction(RIGHT)
    snake.move()
    assert snake.head == (100, 90)

    snake.set_direction(DOWN)
    snake.move()
    assert snake.head == (100, 100)


def test_snake_prevent_reverse_direction():
    snake = Snake(direction=LEFT)
    snake.set_direction(RIGHT)
    assert snake.direction == LEFT

    snake.set_direction(UP)
    assert snake.direction == UP
    snake.set_direction(DOWN)
    assert snake.direction == UP


def test_snake_invalid_direction():
    snake = Snake(direction=999)
    assert snake.compute_next_head() == snake.head


def test_snake_grow_and_self_collision():
    snake = Snake(initial_body=[(100, 100), (110, 100), (110, 110), (100, 110), (100, 100)])
    assert snake.collides_with_self() is True

    snake_ok = Snake(initial_body=[(100, 100), (110, 100)])
    assert snake_ok.collides_with_self() is False
    snake_ok.grow()
    assert len(snake_ok.body) == 3
    assert snake_ok.body[-1] == (0, 0)


def test_snake_out_of_bounds():
    assert Snake(initial_body=[(-10, 100)]).is_out_of_bounds() is True
    assert Snake(initial_body=[(600, 100)]).is_out_of_bounds() is True
    assert Snake(initial_body=[(100, -10)]).is_out_of_bounds() is True
    assert Snake(initial_body=[(100, 600)]).is_out_of_bounds() is True
    assert Snake(initial_body=[(0, 0)]).is_out_of_bounds() is False
    assert Snake(initial_body=[(590, 590)]).is_out_of_bounds() is False


def test_snake_collides_with_other():
    player = Snake(initial_body=[(110, 100), (120, 100)])
    other_short = Snake(initial_body=[(100, 100), (110, 100)])
    assert player.collides_with_other(other_short) is False

    other_long = Snake(initial_body=[(100, 100), (110, 100), (120, 100), (130, 100)])
    assert player.collides_with_other(other_long) is True


def test_ai_snake_decision_and_movement():
    ai = AISnake(initial_body=[(100, 100), (110, 100), (120, 100)], direction=LEFT)
    # Maçã abaixo e à esquerda
    ai.decide_direction((50, 150))
    assert ai.direction == DOWN

    # Maçã acima
    ai.decide_direction((50, 50))
    assert ai.direction == UP

    # Maçã à direita (agora direção é UP, então pode ir para RIGHT)
    ai.decide_direction((150, 50))
    assert ai.direction == RIGHT

    # Maçã à esquerda (direção é RIGHT, não deve inverter direto para LEFT)
    ai.decide_direction((50, 50))
    assert ai.direction == RIGHT


def test_ai_snake_update_position_safe_and_obstacle():
    rng = random.Random(1)
    ai = AISnake(initial_body=[(100, 100), (110, 100), (120, 100)], direction=LEFT, rng=rng)
    ai.update_position(player_body=[(300, 300)])
    assert ai.head == (90, 100)

    # Colisão com borda força teleporte aleatório
    ai_edge = AISnake(initial_body=[(0, 100), (10, 100), (20, 100)], direction=LEFT, rng=rng)
    ai_edge.update_position(player_body=[(300, 300)], random_pos_fn=lambda: (250, 250))
    assert ai_edge.head == (250, 250)

    # Quando should_move é False não altera posição
    ai_stopped = AISnake(initial_body=[(100, 100), (110, 100), (120, 100)], direction=LEFT)
    ai_stopped.should_move = False
    ai_stopped.update_position(player_body=[])
    assert ai_stopped.head == (100, 100)

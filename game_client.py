#game_client.py

import pygame
import socket
from config import *
from enemy import Enemy
from utils import load_scores, save_score

class GameClient:
    def __init__(self, host, port,nickname):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Yasser's Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        
        self.x = WINDOW_SIZE[0] // 2
        self.y = WINDOW_SIZE[1] - PLAYER_SIZE - 10
        self.score = 0
        self.game_over = False
        self.enemies = []
        self.last_spawn_time = 0
        self.nickname = nickname  # Store the player's nickname
        self.spawn_rate = INITIAL_SPAWN_RATE
        self.high_scores = load_scores()

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += PLAYER_SPEED
        self.x = max(0, min(self.x, WINDOW_SIZE[0] - PLAYER_SIZE))

    def spawn_enemies(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_rate:
            self.enemies.append(Enemy())
            self.last_spawn_time = current_time
            self.spawn_rate = max(400, self.spawn_rate - 1)

    def update_enemies(self):
        for enemy in self.enemies[:]:
            if enemy.update():
                self.enemies.remove(enemy)
                self.score += 1

    def check_collisions(self):
        player_rect = pygame.Rect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                self.game_over = True
                save_score(self.score)
                break

    def draw_game(self):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, PLAYER_COLOR, (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, ENEMY_COLOR, (enemy.x, enemy.y, ENEMY_SIZE, ENEMY_SIZE))
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        # Clear the screen with the background color
        self.screen.fill(BACKGROUND_COLOR)

        # Render "Game Over" message
        game_over_text = self.font.render('Game Over!', True, (0, 0, 0))
        self.screen.blit(
            game_over_text,
            (WINDOW_SIZE[0] // 2 - game_over_text.get_width() // 2, WINDOW_SIZE[1] // 2 - 60)
        )

        # Render the player's final score
        score_text = self.font.render(f'Final Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(
            score_text,
            (WINDOW_SIZE[0] // 2 - score_text.get_width() // 2, WINDOW_SIZE[1] // 2)
        )

        # Render prompt to restart the game
        restart_text = self.font.render('Press SPACE to restart', True, (0, 0, 0))
        self.screen.blit(
            restart_text,
            (WINDOW_SIZE[0] // 2 - restart_text.get_width() // 2, WINDOW_SIZE[1] // 2 + 60)
        )

        # Display high scores
        y_offset = WINDOW_SIZE[1] // 2 + 120
        title_text = self.font.render('High Scores:', True, (0, 0, 0))
        self.screen.blit(
            title_text,
            (WINDOW_SIZE[0] // 2 - title_text.get_width() // 2, y_offset)
        )

        # Render the top 5 high scores
        for i, score_data in enumerate(self.high_scores[:5]):
            nickname = score_data.get("nickname", "Anonymous")  # Default to "Anonymous" if no nickname
            score = score_data["score"]
            score_line = self.font.render(f'{i + 1}. {nickname}: {score}', True, (0, 0, 0))
            self.screen.blit(
                score_line,
                (WINDOW_SIZE[0] // 2 - score_line.get_width() // 2, y_offset + 40 * (i + 1))
            )

    def reset_game(self):
        self.x = WINDOW_SIZE[0] // 2
        self.y = WINDOW_SIZE[1] - PLAYER_SIZE - 10
        self.score = 0
        self.enemies.clear()
        self.game_over = False
        self.spawn_rate = INITIAL_SPAWN_RATE

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

            if not self.game_over:
                self.handle_movement()
                self.spawn_enemies()
                self.update_enemies()
                self.check_collisions()
                self.draw_game()
            else:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        save_score(self.score, self.nickname)
        pygame.quit()
        self.socket.close()

# config.py

WINDOW_SIZE = (800, 600)
PLAYER_SIZE = 50
PLAYER_SPEED = 7
PLAYER_COLOR = (0, 0, 255)
ENEMY_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
ENEMY_SIZE = 30
ENEMY_SPEED = 10
INITIAL_SPAWN_RATE = 1000
SCORES_FILE = "highscores.json"
POWERUP_SIZE = 20
POWERUP_SPAWN_RATE = 10000  # Spawn every 10 seconds
POWERUP_COLORS = {
    'shield': (0, 255, 255),     # Cyan
    'slow': (255, 255, 0),       # Yellow
    'score_boost': (255, 165, 0)  # Orange
}
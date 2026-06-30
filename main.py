import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from shot import Shot
from asteroidfield import AsteroidField


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 30)
    header_font = pygame.font.Font(None, 60)
    dt = 0.0
    points = 0
    game_over = False

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)
    AsteroidField.containers = (updatable)

    player = Player(SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if not game_over:    
            updatable.update(dt)    
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()
                        points += 100
                if player.collides_with(asteroid):
                    log_event("player_hit")
                    print("Game over!")
                    game_over = True

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f"points: {points}", True, "White")
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = header_font.render("GAME OVER", True, "White")
            text_rect = game_over_text.get_rect(
                center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()
        
        # framerate 60 FPS
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()

import socket
import pygame

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client - Multiplayer Ping Pong")

# Client setup
SERVER_IP = "192.168.1.10"
SERVER_PORT = 5000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

# Game variables
paddle1_y, paddle2_y, ball_x, ball_y = HEIGHT // 2, HEIGHT // 2, WIDTH // 2, HEIGHT // 2


# Draw game state
def draw_window(paddle1_y, paddle2_y, ball_x, ball_y):
    WIN.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(WIN, WHITE, (20, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(WIN, WHITE, (WIDTH - 40, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.circle(WIN, WHITE, (ball_x, ball_y), BALL_RADIUS)

    pygame.display.update()


def main():
    global paddle2_y, paddle1_y, ball_x, ball_y

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(120)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player 2 movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddle2_y - 5 > 0:
            paddle2_y -= 5
        if keys[pygame.K_DOWN] and paddle2_y + PADDLE_HEIGHT + 5 < HEIGHT:
            paddle2_y += 5

        # Send Player 2's paddle position to the server
        client.send(str(paddle2_y).encode())

        # Receive updated game state from the server
        try:
            game_state = client.recv(1024).decode()
            paddle1_y, paddle2_y, ball_x, ball_y = map(int, game_state.split(","))
        except:
            pass

        # Draw the updated game state
        draw_window(paddle1_y, paddle2_y, ball_x, ball_y)

    pygame.quit()


if __name__ == "__main__":
    main()

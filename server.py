import socket
import pygame
import threading
import time
# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Server - Multiplayer Ping Pong")

# Server setup
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()

# Game variables
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5
paddle1_y, paddle2_y = HEIGHT // 2, HEIGHT // 2


# Draw game state
def draw_window(paddle1_y, paddle2_y, ball_x, ball_y):
    WIN.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(WIN, WHITE, (20, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(WIN, WHITE, (WIDTH - 40, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.circle(WIN, WHITE, (ball_x, ball_y), BALL_RADIUS)

    pygame.display.update()


# Handle client connection
def handle_client(conn):
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_dx, ball_dy
    conn.send(f"{paddle1_y},{paddle2_y},{ball_x},{ball_y}".encode())

    while True:
        try:
            # Receive Player 2's paddle position from the client
            data = conn.recv(1024).decode()
            if not data:
                break
            paddle2_y = int(data)

            # Ball movement
            ball_x += ball_dx
            ball_y += ball_dy

            # Ball collision with top/bottom walls
            if ball_y <= 0 or ball_y >= HEIGHT:
                ball_dy *= -1
            # Ball collision with paddles
            if ball_x <= 40 and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT:
                ball_dx *= -1
            if ball_x >= WIDTH - 40 and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT:
                ball_dx *= -1
            # Ball out of bounds
            if ball_x <= 0 or ball_x >= WIDTH:
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2

            # Send game state to client
            conn.send(f"{paddle1_y},{paddle2_y},{ball_x},{ball_y}".encode())

        except Exception as e:
            print(f"[EXCEPTION] {e}")
            break

    conn.close()


# Start server and control Player 1 (server side)
def start():
    global paddle1_y
    print("[STARTING] Server is starting and waiting for a connection...")
    conn, addr = server.accept()
    print(f"[NEW CONNECTION] {addr} connected as Player 2.")

    client_thread = threading.Thread(target=handle_client, args=(conn,))
    client_thread.start()

    # Server controls Player 1's paddle
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Move Player 1's paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y - 5 > 0:
            paddle1_y -= 5
        if keys[pygame.K_s] and paddle1_y + PADDLE_HEIGHT + 5 < HEIGHT:
            paddle1_y += 5

        # Draw the game window
        draw_window(paddle1_y, paddle2_y, ball_x, ball_y)

    pygame.quit()


if __name__ == "__main__":
    start()

# import socket
# import pygame
# import threading

# # Constants
# WIDTH, HEIGHT = 800, 600
# BALL_RADIUS = 10
# PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# # Initialize pygame
# pygame.init()
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Server - Multiplayer Ping Pong")

# # Font for score display (initialize after pygame.init())
# FONT = pygame.font.SysFont(None, 50)

# # Server setup
# SERVER_IP = "0.0.0.0"
# SERVER_PORT = 5555
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((SERVER_IP, SERVER_PORT))
# server.listen()

# # Game variables
# ball_x, ball_y = WIDTH // 2, HEIGHT // 2
# ball_dx, ball_dy = 5, 5
# paddle1_y, paddle2_y = HEIGHT // 2, HEIGHT // 2
# score1, score2 = 0, 0  # Player scores


# # Draw game state
# def draw_window(paddle1_y, paddle2_y, ball_x, ball_y, score1, score2):
#     WIN.fill(BLACK)

#     # Draw center line
#     for y in range(0, HEIGHT, 20):
#         pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 2, y, 4, 10))

#     # Draw paddles
#     pygame.draw.rect(WIN, WHITE, (20, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
#     pygame.draw.rect(WIN, WHITE, (WIDTH - 40, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

#     # Draw ball
#     pygame.draw.circle(WIN, WHITE, (ball_x, ball_y), BALL_RADIUS)

#     # Draw scores
#     score_text1 = FONT.render(str(score1), True, WHITE)
#     score_text2 = FONT.render(str(score2), True, WHITE)
#     WIN.blit(score_text1, (WIDTH // 4, 20))
#     WIN.blit(score_text2, (3 * WIDTH // 4 - score_text2.get_width(), 20))

#     pygame.display.update()


# # Handle client connection
# def handle_client(conn):
#     global paddle1_y, paddle2_y, ball_x, ball_y, ball_dx, ball_dy, score1, score2
#     conn.send(f"{paddle1_y},{paddle2_y},{ball_x},{ball_y}".encode())

#     while True:
#         try:
#             # Receive Player 2's paddle position from the client
#             data = conn.recv(1024).decode()
#             if not data:
#                 break
#             paddle2_y = int(data)

#             # Ball movement
#             ball_x += ball_dx
#             ball_y += ball_dy

#             # Ball collision with top/bottom walls
#             if ball_y <= 0 or ball_y >= HEIGHT:
#                 ball_dy *= -1
#             # Ball collision with paddles
#             if ball_x <= 40 and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT:
#                 ball_dx *= -1
#             if ball_x >= WIDTH - 40 and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT:
#                 ball_dx *= -1
#             # Ball out of bounds (scoring)
#             if ball_x <= 0:
#                 score2 += 1
#                 ball_x, ball_y = WIDTH // 2, HEIGHT // 2
#                 ball_dx = -5
#             elif ball_x >= WIDTH:
#                 score1 += 1
#                 ball_x, ball_y = WIDTH // 2, HEIGHT // 2
#                 ball_dx = 5

#             # Send game state to client
#             conn.send(f"{paddle1_y},{paddle2_y},{ball_x},{ball_y},{score1},{score2}".encode())

#         except Exception as e:
#             print(f"[EXCEPTION] {e}")
#             break

#     conn.close()


# # Start server and control Player 1 (server side)
# def start():
#     global paddle1_y
#     print("[STARTING] Server is starting and waiting for a connection...")
#     conn, addr = server.accept()
#     print(f"[NEW CONNECTION] {addr} connected as Player 2.")

#     client_thread = threading.Thread(target=handle_client, args=(conn,))
#     client_thread.start()

#     # Server controls Player 1's paddle
#     clock = pygame.time.Clock()

#     run = True
#     while run:
#         clock.tick(45)

#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False

#         # Move Player 1's paddle
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_w] and paddle1_y - 5 > 0:
#             paddle1_y -= 10
#         if keys[pygame.K_s] and paddle1_y + PADDLE_HEIGHT + 5 < HEIGHT:
#             paddle1_y += 10

#         # Draw the game window
#         draw_window(paddle1_y, paddle2_y, ball_x, ball_y, score1, score2)

#     pygame.quit()


# if __name__ == "__main__":
#     start()


import socket
import pygame
import threading
import tkinter as tk
from tkinter import messagebox

# Constants for the game
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SERVER_PORT = 5555  # Fixed port for both server and client

# Initialize pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Ping Pong")

# Game variables
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5
paddle1_y, paddle2_y = HEIGHT // 2, HEIGHT // 2

# Function to draw the game state
def draw_window(paddle1_y, paddle2_y, ball_x, ball_y):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, (20, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # Left paddle
    pygame.draw.rect(WIN, WHITE, (WIDTH - 40, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # Right paddle
    pygame.draw.circle(WIN, WHITE, (ball_x, ball_y), BALL_RADIUS)  # Ball
    pygame.display.update()

# Server function
def run_server():
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_dx, ball_dy
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", SERVER_PORT))
    server.listen()
    print("[SERVER STARTED] Waiting for connection...")

    conn, addr = server.accept()
    print(f"[NEW CONNECTION] {addr} connected as Player 2.")
    conn.send(f"{paddle1_y},{paddle2_y},{ball_x},{ball_y}".encode())

    def handle_client():
        global paddle1_y, paddle2_y, ball_x, ball_y, ball_dx, ball_dy
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                paddle2_y = int(data)
                ball_x += ball_dx
                ball_y += ball_dy

                # Ball collision with top and bottom walls
                if ball_y <= 0 or ball_y >= HEIGHT:
                    ball_dy *= -1

                # Ball collision with paddles
                if ball_x <= 40 and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT:
                    ball_dx *= -1
                if ball_x >= WIDTH - 40 and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT:
                    ball_dx *= -1

                # Ball out of bounds, reset position
                if ball_x <= 0 or ball_x >= WIDTH:
                    ball_x, ball_y = WIDTH // 2, HEIGHT // 2

                conn.send(f"{paddle1_y},{paddle2_y},{ball_x},{ball_y}".encode())
        except:
            print("[SERVER] Client disconnected.")
        finally:
            conn.close()
            pygame.quit()

    client_thread = threading.Thread(target=handle_client)
    client_thread.start()

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conn.close()  # Close connection on server quit
                pygame.quit()
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y - 5 > 0:
            paddle1_y -= 10
        if keys[pygame.K_s] and paddle1_y + PADDLE_HEIGHT + 5 < HEIGHT:
            paddle1_y += 10
        draw_window(paddle1_y, paddle2_y, ball_x, ball_y)

# Client function
def run_client(server_ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, SERVER_PORT))
    except:
        messagebox.showerror("Error", "Unable to connect to the server.")
        return
    
    global paddle1_y, paddle2_y, ball_x, ball_y

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                pygame.quit()
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddle2_y - 5 > 0:
            paddle2_y -= 5
        if keys[pygame.K_DOWN] and paddle2_y + PADDLE_HEIGHT + 5 < HEIGHT:
            paddle2_y += 5
        try:
            client.send(str(paddle2_y).encode())
            game_state = client.recv(1024).decode()
            if not game_state:
                raise ConnectionError("Server closed the connection.")
            paddle1_y, paddle2_y, ball_x, ball_y = map(int, game_state.split(","))
        except (ConnectionError, OSError):
            print("[CLIENT] Server disconnected or error occurred.")
            break
        draw_window(paddle1_y, paddle2_y, ball_x, ball_y)

    client.close()
    pygame.quit()

# Start the GUI
def start_gui():
    def start_game():
        mode = mode_var.get()
        ip_address = ip_entry.get()

        if mode == "server":
            threading.Thread(target=run_server, daemon=True).start()
            messagebox.showinfo("Server", "Server started successfully!")
        elif mode == "client":
            if not ip_address:
                messagebox.showerror("Error", "Please enter the server IP address.")
            else:
                threading.Thread(target=run_client, args=(ip_address,), daemon=True).start()
                messagebox.showinfo("Client", f"Attempting to connect to server at {ip_address}")

    def toggle_ip_entry():
        if mode_var.get() == "client":
            ip_entry_label.pack()
            ip_entry.pack()
        else:
            ip_entry_label.pack_forget()
            ip_entry.pack_forget()

    app = tk.Tk()
    app.title("Multiplayer Ping Pong")

    app.geometry("200x200")

    mode_var = tk.StringVar(value="server")
    tk.Label(app, text="Select Mode:").pack()
    tk.Radiobutton(app, text="Server", variable=mode_var, value="server", command=toggle_ip_entry).pack()
    tk.Radiobutton(app, text="Client", variable=mode_var, value="client", command=toggle_ip_entry).pack()

    ip_entry_label = tk.Label(app, text="Server IP Address (for Client Mode):")
    ip_entry = tk.Entry(app)

    start_button = tk.Button(app, text="Start Game", command=start_game)
    start_button.pack()

    toggle_ip_entry()  # Set initial visibility
    app.mainloop()

# Run the GUI to choose mode
if __name__ == "__main__":
    start_gui()

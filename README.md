# Network-Based Ping Pong Game

This project is a simple network-based ping pong game that consists of a server and a client component. The server hosts the game, and the client connects to the server using its IP address. The game allows two players to connect and play using two separate computers on the same network.

## Project Structure
- **`server.py`**: The server file that hosts the game.
- **`client.py`**: The client file that connects to the server and allows the player to interact with the game.

## How It Works
- The server is hosted on the local network and listens for incoming client connections.
- The client program connects to the server using the IP address of the server's computer.
- Once connected, the game starts, and players can play ping pong against each other.

## Steps to Run
- Clone the repository
- Enter the ip address of host pc in the client.py file.
- Run server.py on host pc
- Run client.py on client pc
- Use W and S keys to control the paddle in host pc
- Use Up and Down keys to control the paddle in client pc

## Troubleshooting
- Ensure that the client is connected to correct ip address of ther server pc. Use **`ipconfig`** to check the local ip of the host pc.
- Connecting to 5 Ghz network is recommended.
- Disabling fire wall in both Host and client pc can make the game run smoothly and prevent errors and blocking.

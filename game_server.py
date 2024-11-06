# game_server.py

import socket
import threading
import json
from config import WINDOW_SIZE, PLAYER_SIZE

class GameServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.players = {}
        self.lock = threading.Lock()
        print(f"Server listening on {host}:{port}")

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    def handle_client(self, client_socket, address):
        player_id = str(address)
        with self.lock:
            self.players[player_id] = {
                'x': WINDOW_SIZE[0] // 2,
                'y': WINDOW_SIZE[1] - PLAYER_SIZE - 10,
                'score': 0
            }

        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                try:
                    message = json.loads(data)
                    if message['type'] == 'update':
                        with self.lock:
                            self.players[player_id].update(message)
                    
                    client_socket.sendall(json.dumps(self.players[player_id]).encode())

                except json.JSONDecodeError:
                    print(f"Invalid JSON received: {data}")

        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            with self.lock:
                if player_id in self.players:
                    del self.players[player_id]
            client_socket.close()

# main.py

from game_server import GameServer
from game_client import GameClient

def main():
    mode = input("Enter 's' for server mode or 'c' for client mode: ").lower()
    host = input("Enter IP address: ")
    port = int(input("Enter port number: "))

    if mode == 's':
        server = GameServer(host, port)
        server.start()
    elif mode == 'c':
        client = GameClient(host, port)
        client.run()
    else:
        print("Invalid mode. Enter 's' or 'c'.")

if __name__ == "__main__":
    main()

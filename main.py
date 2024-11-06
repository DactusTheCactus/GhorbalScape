# main.py

from game_server import GameServer
from game_client import GameClient

def main():
    mode = input("Enter 's' for server mode or 'c' for client mode:").lower()
    startShortcut = input("Do you want the use the fast Start? | Y/N | \n").lower()
    
    if (startShortcut == 'y' or startShortcut == 'Yes' or startShortcut == "ye"):
        host = "localhost"
        port = 20000
    else:
        host = input("Enter IP address: ")
        port = int(input("Enter port number: "))

    if mode == 's':
        server = GameServer(host, port)
        server.start()
    elif mode == 'c':
        nickname = input("Enter your nickname: ")  # New nickname prompt
        client = GameClient(host, port, nickname)   # Pass nickname to GameClient
        client.run()
    else:
        print("Invalid mode. Enter 's' or 'c'.")

if __name__ == "__main__":
    main()

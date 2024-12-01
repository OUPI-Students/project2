import socket
import random

HOST = '127.0.0.1'
PORT = 65433  # Updated to match the new server port
choices = ["rock", "paper", "scissors"]

def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(client_socket.recv(1024).decode())

        for round_num in range(1, 11):  # Play 10 rounds
            # Wait for server prompt to make a pick
            server_prompt = client_socket.recv(1024).decode()
            print(server_prompt)

            pick = random.choice(choices)
            print(f"Round {round_num}: Sending pick: {pick}")
            client_socket.sendall(pick.encode())

            # Receive acknowledgment from server for the current round
            server_response = client_socket.recv(1024).decode()
            print(server_response)

        print(client_socket.recv(1024).decode())
    
    except (socket.error, BrokenPipeError) as e:
        print(f"Connection lost: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
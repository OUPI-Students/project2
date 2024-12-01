import socket
import random

# List of valid choices
choices = ['R', 'P', 'S']

# Function to handle client-side game logic
def start_client():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    try:
        # Receive initial welcome message from the server
        message = client_socket.recv(1024).decode()
        print(message)

        for round_number in range(1, 11):  # Play 10 rounds
            # Get player's choice (could be random or heuristic)
            choice = random.choice(choices)  # Random choice for simplicity
            print(f"Round {round_number}: Player choice is {choice}")
            
            # Send the choice to the server
            client_socket.send(choice.encode())
            
            # Wait for the server's response (result of the round)
            result = client_socket.recv(1024).decode()
            print(result)
    
    finally:
        # Close the connection after 10 rounds
        client_socket.close()
        print("Game over!")

if __name__ == '__main__':
    start_client()

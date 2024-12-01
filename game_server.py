import socket
import threading
from flask import Flask, render_template

app = Flask(__name__)

# Global variables to track game state
rounds = []
history = []

# Function to handle game logic and communication with clients
def handle_client(client_socket, client_address, client_number):
    global rounds

    # Send initial message to client
    client_socket.send(f"Welcome to Rock Paper Scissors, Player {client_number}!\n".encode())

    for round_number in range(1, 11):  # Play 10 rounds
        client_socket.send(f"Round {round_number}: Choose Rock (R), Paper (P), or Scissors (S): ".encode())
        choice = client_socket.recv(1024).decode().strip().upper()

        # Add the player's choice to the rounds list
        rounds.append(choice)

        # If both players have chosen, evaluate the round result
        if len(rounds) == 2:  # Two players have chosen
            result = evaluate_round(rounds[0], rounds[1])
            history.append(result)

            # Reset for next round
            rounds = []

            # Send result to both clients
            for cs in [client_socket, other_client_socket]:
                cs.send(f"Round result: {result}\n".encode())

    client_socket.close()

# Function to evaluate round results
def evaluate_round(player1_choice, player2_choice):
    rules = {
        ('R', 'S'): 'Player 1 wins!',
        ('S', 'R'): 'Player 2 wins!',
        ('P', 'R'): 'Player 1 wins!',
        ('R', 'P'): 'Player 2 wins!',
        ('S', 'P'): 'Player 1 wins!',
        ('P', 'S'): 'Player 2 wins!',
    }

    if player1_choice == player2_choice:
        return "It's a draw!"
    return rules.get((player1_choice, player2_choice), "Invalid choice")

# Flask route to show the results in a web interface
@app.route('/')
def index():
    return render_template('index.html', history=history)

# Start server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(2)

    print("Server started, waiting for players...")
    
    while True:
        client_socket, client_address = server.accept()
        print(f"Player connected: {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address, len(history)+1)).start()

# Run server and Flask interface
if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    app.run(debug=True, use_reloader=False)

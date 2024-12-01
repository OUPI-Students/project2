from flask import Flask, render_template
import socket
import threading
import time

# Flask app setup
app = Flask(__name__)
results = []  # Store game results to be displayed on the web page
results_lock = threading.Lock()
results_calculated = False  # Flag to ensure results are calculated only once

# Server setup
HOST = '127.0.0.1'
PORT = 65433  # Changed the port number to avoid conflicts
rounds = 10
clients = []
picks = [[], []]  # Store picks for player 1 and player 2
lock = threading.Lock()

# Function to handle each client's connection
def handle_client(client_socket, client_address, client_id):
    try:
        print(f"Player {client_id} connected from {client_address}.")
        client_socket.sendall(f"Welcome, Player {client_id}! Waiting for the other player...\n".encode())

        # Wait for both players to connect
        while len(clients) < 2:
            time.sleep(0.1)

        client_socket.sendall(b"Both players are connected! The game will now begin.\n")

        for round_num in range(1, rounds + 1):
            # Ask for a pick for the current round
            client_socket.sendall(f"Round {round_num}: Make your pick (rock, paper, scissors):\n".encode())
            pick = client_socket.recv(1024).decode().strip().lower()

            # Validate the pick to ensure it's correct
            while pick not in ["rock", "paper", "scissors"]:
                client_socket.sendall(b"Invalid pick. Please choose 'rock', 'paper', or 'scissors':\n")
                pick = client_socket.recv(1024).decode().strip().lower()

            print(f"Player {client_id} chose '{pick}' in round {round_num}.")

            # Store the player's pick for the current round
            with lock:
                picks[client_id - 1].append(pick)

            # Wait for both players to submit their picks for the round
            while len(picks[0]) < round_num or len(picks[1]) < round_num:
                time.sleep(0.1)

            # Send acknowledgment to client to indicate round is complete
            client_socket.sendall(f"Round {round_num} complete. Waiting for the next round...\n".encode())

        client_socket.sendall(b"Thanks for playing! Waiting for the results...\n")

    except (socket.error, BrokenPipeError) as e:
        print(f"Connection with Player {client_id} lost: {e}")

    finally:
        client_socket.close()

    # Check if both players' results are in to calculate
    with lock:
        if len(picks[0]) == rounds and len(picks[1]) == rounds and not results_calculated:
            calculate_results()

# TCP server to manage connections
def start_server():
    global clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow the address to be reused
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(2)  # Only accept two players
    print(f"Server listening on {HOST}:{PORT}")

    while len(clients) < 2:  # Wait for exactly two players
        client_socket, client_address = server_socket.accept()
        client_id = len(clients) + 1
        clients.append((client_socket, client_address))
        threading.Thread(target=handle_client, args=(client_socket, client_address, client_id)).start()

    print("Both players connected! Starting the game...")

# Function to calculate results
def calculate_results():
    global picks, results, results_calculated
    
    for i in range(rounds):
        p1 = picks[0][i]
        p2 = picks[1][i]

        if p1 == p2:
            result = f"Round {i + 1}: Draw"
        elif (p1 == "rock" and p2 == "scissors") or \
             (p1 == "paper" and p2 == "rock") or \
             (p1 == "scissors" and p2 == "paper"):
            result = f"Round {i + 1}: Player 1 wins"
        else:
            result = f"Round {i + 1}: Player 2 wins"

        with results_lock:
            results.append(result)

    results_calculated = True  # Set the flag to indicate results have been calculated

    # Debug output to verify results are being calculated
    print("Game Results Calculated:")
    for result in results:
        print(result)

# Flask route to display results
@app.route('/')
def show_results():
    with results_lock:
        if not results:
            return """<h1>Rock Paper Scissors Game Results</h1><p>No results available yet. Please wait for the game to finish.</p>"""
        return render_template('index.html', history=results)

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Start the Flask web server without debug mode
    app.run(port=5000, debug=False)


# Project 2

## Overview

This project implements a network-based Rock Paper Scissors game using Python's socket programming. The game involves two clients connecting to a server and playing 10 rounds of Rock Paper Scissors. The server handles multiple client connections, collects their picks for each round, displays the round results in real-time, and maintains a history of the results. A Flask-based web interface is used to display the game results.

## Files

- `README.md`: Project documentation
- `game_server.py`: The server script that manages client connections, game logic, and stores the history of results.
- `game_client.py`: The client script that connects to the server, sends player choices for each round, and receives the results.
- `game_ui.py`: The Flask web interface that displays the results of the game in real-time.
- `templates/index.html`: The HTML template used by the Flask web interface to display the round history.

## Requirements

- Python 3.x
- Flask (for the web interface)

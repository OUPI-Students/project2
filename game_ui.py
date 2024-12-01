from flask import Flask, render_template
from threading import Lock

app = Flask(__name__)

# Global variables to track game state
rounds_history = []
history_lock = Lock()

# Route to show the results in the web interface
@app.route('/')
def index():
    # Lock to safely access the shared history variable
    with history_lock:
        return render_template('index.html', history=rounds_history)

# Function to add a round result to the history (called by the server)
def add_round_result(result):
    with history_lock:
        rounds_history.append(result)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

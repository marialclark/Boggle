from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
boggle_game = Boggle()

app.config['SECRET_KEY'] = "secrets"

@app.route('/')
def home():
    """Renders Boggle board and places it in session. Ensures that 
    it knows to restart games played & highscore if new session."""
    board = boggle_game.make_board()
    session['board'] = board

    if 'games_played' not in session:
        session['games_played'] = 0
    if 'highest_score' not in session:
        session['highest_score'] = 0

    print("Board stored in session:", board) #Debugging

    return render_template("base.html", board=board)

@app.route('/submit-guess', methods=["POST"])
def submitted_guess():
    """Retrieves guess from front end, checks if the word is 
    valid, then returns the result."""
    guess = request.json['guess']
    board = session['board']
    result = boggle_game.check_valid_word(board, guess)

    print(f"Guess: {guess}, Result: {result}, Board: {board}") #Debugging

    return jsonify({'result':result})

@app.route('/score', methods=["POST"])
def score():
    """Retrieves score from the front end and displays it to the user."""
    score = request.json["score"]
    return jsonify({'Current Score:': score})

@app.route('/update-stats', methods=["POST"])
def update_stats():
    """Retrieves data from the front end and updates the session
    with the amount of games played and highscore."""
    data = request.json 
    current_score = data.get('score', 0)
    
    session['games_played'] += 1
    
    if current_score > session['highest_score']:
        session['highest_score'] = current_score
    
    print(f"Games Played: {session['games_played']}, Highest Score:{session['highest_score']}")  # Debugging
    
    return jsonify({'games_played': session['games_played'], 'highest_score': session['highest_score']})

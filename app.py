from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkeysecretkey"


@app.route("/")
def homepage():
    """Show board."""

    #use functions in boggle class to make the game board. Not sure where boggle_game comes from, I assume it's just a filler name to run the make_board() function.
    board = boggle_game.make_board()
    #set the session's board to be the newly created board so the created board can be saved when the page is refreshed
    session['board'] = board
    #use session.get to get the highscore that is stored, if there's no highscore, have it be set to 0.
    highscore = session.get("highscore", 0)
    #get the number of plays from the session, if none then store 0 as the value
    nplays = session.get("nplays", 0)

    return render_template("index.html", board = board, 
                            highscore = highscore,
                            nplays = nplays)

@app.route("/check-word")
def check_word():
    """Check if word is in the dictionary"""

    #when the user types a word, it is retrieved using request.args["word"] and stored into var word
    word = request.args["word"]
    # the board is set to be the "board" saved in the session
    board = session["board"]
    # using check_valid_word function from boggle.py will verify whether word is valid using the board and word variables
    response = boggle_game.check_valid_word(board, word)

    #returns a jsonified result and response which will be returned as a string.
    return jsonify({'result': response})

@app.route("/post-score", methods = ["POST"])
def post_score():
    """Receive score, update nplays, and update the high score appropriately"""

    #set score using request.json which will set the score according to the current score
    score = request.json["score"]
    # highscore is set to the highscore stored in the session or 0 if no highscore
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    #increment nplays once the game is finished
    session['nplays'] = nplays + 1
    #set the new highscore in the session to be score or highscore, whichever is higher
    session['highscore'] = max(score, highscore)

    #returns a string that equals score if it's higher, if not return highscore
    return jsonify(brokeRecord = score > highscore)
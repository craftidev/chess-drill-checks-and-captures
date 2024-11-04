from flask import Flask, json, render_template, jsonify, request, session, make_response
import chess

app = Flask(__name__)
app.secret_key = b'make_a_secret_key_for_prod_here'

@app.route("/new_position")
def new_position():
    fen = "4k3/2bppp2/8/8/3PPP2/3N4/3K4/8 w - - 0 1"
    session["fen"] = fen
    board = chess.Board(fen)

    white_to_play = board.turn
    square_names = [chess.square_name(square) for square in chess.SQUARES]
    if white_to_play:
        square_names.reverse()

    pieces = {}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = 'w' if piece.color == chess.WHITE else 'b'
            piece_name = color + piece.symbol().upper()
            pieces[chess.square_name(square)] = piece_name

    return render_template(
        "partials/board.html",
        fen = fen,
        pieces = pieces,
        square_names = square_names,
    )

def get_opponent_checks_and_captures(board):
    board.turn = not board.turn
    opponent_moves = []
    for move in board.legal_moves:
        if board.is_capture(move):
            opponent_moves.append(move.uci())
            continue
        elif board.gives_check(move):
            opponent_moves.append(move.uci())
    board.turn = not board.turn

    return opponent_moves

@app.route("/validate_arrows", methods=["POST"])
def validate_arrows():
    data = request.form
    arrows_json = data.get("arrows")
    arrows = json.loads(arrows_json) if arrows_json else []
    fen = session.get("fen")

    board = chess.Board(fen)
    required_moves = get_opponent_checks_and_captures(board)
    is_correct = sorted(required_moves) == sorted(arrows)

    streak = int(session.get("streak", 0))
    if is_correct:
        streak += 1
        message = "Correct!"
        message_class = "correct-message"
    else:
        streak = 0
        message = "Incorrect, try again."
        message_class = "incorrect-message"

    session["message"] = message
    session["message_class"] = message_class
    session["streak"] = streak

    response = make_response()
    response.headers['HX-Trigger'] = 'updateFeedback'

    return response

@app.route("/update_message")
def update_message():
    message = session.get("message", "")
    message_class = session.get("message_class", "")
    return f'<p id="message" class="{ message_class }">{ message }</p>'
@app.route("/update_streak")
def update_streak():
    streak = session.get("streak", 0)
    return f'<span id="streak-counter">{ streak }</span>'
@app.route("/reset_arrows")
def reset_arrows():
    return '<input type="hidden" name="arrows" id="arrows">', 200

@app.route("/")
def main():
    streak = session.get("streak", 0)
    return render_template(
        "index.html",
        streak = streak,
    )

if __name__ == "__main__":
    app.run(debug=True)

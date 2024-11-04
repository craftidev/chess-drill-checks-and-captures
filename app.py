import random
from flask import Flask, json, render_template, request, session, make_response
import chess
import chess.pgn

app = Flask(__name__)
app.secret_key = b'make_a_secret_key_for_prod_here'

def select_random_position(pgn_file_path = "static/resources/WorldChamp2023.pgn"):
    with open(pgn_file_path) as pgn_file:
        games = list(chess.pgn.read_game(pgn_file) for _ in range(14))
        random_game = random.choice(games)

    positions = []
    board = random_game.board()
    positions.append(board.fen())

    for move in random_game.mainline_moves():
        board.push(move)
        positions.append(board.fen())

    nasa = 0
    while True:
        nasa += 1
        random_position_fen = random.choice(positions)
        board = chess.Board(random_position_fen)
        board.turn = not board.turn
        if any(board.legal_moves):
            return random_position_fen
        if nasa > 10000:
            print("LOOP error")

@app.route("/new_position")
def new_position():
    fen = select_random_position()
    session["fen"] = fen
    board = chess.Board(fen)
    player_color = "white" if board.turn else "black"

    square_names = [chess.square_name(square) for square in chess.SQUARES]
    if board.turn:
        square_names.reverse()

    pieces = {}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = 'w' if piece.color == chess.WHITE else 'b'
            piece_name = color + piece.symbol().upper()
            pieces[chess.square_name(square)] = piece_name

    board_html = render_template(
        "partials/board.html",
        fen = fen,
        pieces = pieces,
        square_names = square_names,
        player_color = player_color
    )
    button_html = render_template(
        "partials/submit_button.html",
        player_color=player_color,
    )

    response = make_response(f"""
        {board_html}
        <div hx-swap-oob="outerHTML" id="submit-button">
            {button_html}
        </div>
    """)
    response.headers['HX-Trigger'] = 'updateFeedback, resetArrows'
    return response

def get_opponent_checks_and_captures(board):
    board.turn = not board.turn
    opponent_moves = [
        move.uci() for move in board.legal_moves
        if board.is_capture(move) or board.gives_check(move)
    ]
    board.turn = not board.turn
    return opponent_moves

@app.route("/validate_arrows", methods=["POST"])
def validate_arrows():
    arrows = json.loads(request.form.get("arrows", "[]"))
    fen = session.get("fen")
    board = chess.Board(fen)
    required_moves = get_opponent_checks_and_captures(board)
    is_correct = sorted(required_moves) == sorted(arrows)

    streak = session.get("streak", 0) + 1 if is_correct else 0
    message = "Correct!" if is_correct else "Incorrect, try again."
    message_class = "correct-message" if is_correct else "incorrect-message"

    session.update({
        "message": message,
        "message_class": message_class,
        "streak": streak
    })

    response = make_response()
    if is_correct:
        response.headers['HX-Trigger'] = 'updateFeedback, resetArrows, loadNewPosition'
    else:
        response.headers['HX-Trigger'] = 'updateFeedback, resetArrows'
    return response

@app.route("/update_message")
def update_message():
    message = session.get("message", "")
    message_class = session.get("message_class", "")
    return f'<p id="message" class="{ message_class }">{ message }</p>'

@app.route("/update_streak")
def update_streak():
    return f'<span id="streak-counter">{ session.get("streak", 0) }</span>'

@app.route("/reset_arrows")
def reset_arrows():
    return '<input type="hidden" name="arrows" id="arrows" value=[]>', 200

@app.route("/")
def main():
    return render_template("index.html", streak=session.get("streak", 0))

if __name__ == "__main__":
    app.run(debug = True)

from flask import Flask, render_template, jsonify, request
import chess

app = Flask(__name__)

@app.route("/new_position")
def new_position():
    fen = "4k3/2bppp2/8/8/3PPP2/3N4/3K4/8 w - - 0 1"
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
        pieces = pieces,
        square_names = square_names,
    )

@app.route("/validate_arrows", methods=["POST"])
def validate_arrows():
    data = request.json
    arrows = data.get("arrows", [])

    response = {
        "streak_updated": True,
        "message": "Correct" if True else "Incorrect, try again."
    }

    return jsonify(response)

@app.route("/")
def main():
    return render_template(
        "index.html",
        streak = 0,
    )

if __name__ == "__main__":
    app.run(debug=True)

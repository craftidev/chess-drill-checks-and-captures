let startSquare = null;
let arrows = [];


function clearArrows() {
    document.querySelectorAll("connection").forEach(el => el.remove());
}

document.addEventListener('DOMContentLoaded', () => {
    const chessboard = document.getElementById('chessboard');

    if (chessboard) {
        chessboard.addEventListener('mousedown', (event) => {
            if (event.target.classList.contains('square')) {
                startSquare = event.target.id;
            }
        });

        chessboard.addEventListener('mouseup', (event) => {
            if (event.target.classList.contains('square') && startSquare) {
                const endSquare = event.target.id;
                if (startSquare !== endSquare) {
                    if (arrows.includes(startSquare + endSquare)) {
                        // Remove existing arrow if redrawn
                        arrows = arrows.filter(arrow => arrow !== startSquare + endSquare);
                        document.getElementById("arrow-" + startSquare + endSquare).remove();
                    } else {
                        // Add new arrow
                        arrows.push(startSquare + endSquare);
                        drawArrow(startSquare, endSquare);
                    }
                    document.getElementById('arrows').value = JSON.stringify(arrows);
                }
                startSquare = null;
            }
        });
    }
});

function drawArrow(start, end) {
    const newArrow = document.createElement("connection");
    newArrow.setAttribute("from", "#" + start);
    newArrow.setAttribute("to", "#" + end);
    newArrow.setAttribute("tail", "");
    newArrow.setAttribute("color", "brown");
    newArrow.setAttribute("id", "arrow-" + start + end);
    document.body.appendChild(newArrow);
}

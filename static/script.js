let startSquare = null;
let arrows = [];

document.querySelectorAll('.square').forEach(square => {
    square.addEventListener('mousedown', function(event) {
        startSquare = event.currentTarget.id;
    });

    square.addEventListener('mouseup', function(event) {
        const endSquare = event.currentTarget.id;
        if (startSquare && startSquare !== endSquare) {
            arrows.push(startSquare + endSquare);
            drawArrow(startSquare, endSquare);
        }
        startSquare = null;
    });
});

function drawArrow(start, end) {
    const startSquare = document.getElementById(start);
    const endSquare = document.getElementById(end);
    const newArrow = document.createElement("connection")
    newArrow.setAttribute("from", "#" + start)
    newArrow.setAttribute("to", "#" + end)
    newArrow.setAttribute("tail", "")
    newArrow.setAttribute("color", "brown")
    document.body.appendChild(newArrow)
    console.log(start, end);
}

document.getElementById('submit-button').addEventListener('click', function() {
    fetch('/validate_arrows', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ arrows: arrows })
    }).then(response => response.json())
        .then(data => {
            console.log(data);
        });
});

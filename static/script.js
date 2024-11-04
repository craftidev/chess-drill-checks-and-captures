let startSquare = null;
let arrows = [];

document.querySelectorAll('.square').forEach(square => {
    square.addEventListener('mousedown', function(event) {
        startSquare = event.currentTarget.id;
    });

    square.addEventListener('mouseup', function(event) {
        const endSquare = event.currentTarget.id;
        if (startSquare && startSquare !== endSquare) {
            if (arrows.includes(startSquare + endSquare)) {
                for (let index = 0; index < arrows.length; index++) {
                    const element = arrows[index];
                    if (element === startSquare + endSquare) {
                        arrows.splice(index, 1);
                        document.getElementById("arrow-" + element).remove();
                        break;
                    }
                }
            } else {
                arrows.push(startSquare + endSquare);
                drawArrow(startSquare, endSquare);
            }
            document.getElementById('arrows').value = JSON.stringify(arrows);
        }
        startSquare = null;
    });
});

function drawArrow(start, end) {
    const newArrow = document.createElement("connection")
    newArrow.setAttribute("from", "#" + start)
    newArrow.setAttribute("to", "#" + end)
    newArrow.setAttribute("tail", "")
    newArrow.setAttribute("color", "brown")
    newArrow.setAttribute("id", "arrow-" + start + end)
    document.body.appendChild(newArrow)
}

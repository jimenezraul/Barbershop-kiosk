// Get the modal
var barbernoti = document.getElementById("barberNoti");
var barbercompleted = document.getElementById("barberCompleted");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");
var btn2 = document.getElementById("myCompleted");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close2")[0];

var overlay = document.getElementById('outFrame');
var complete = document.getElementById('outOfFrame');

// When the user clicks the button, open the modal
btn.onclick = function () {
    barbernoti.classList = "d-flex barbernoti col-12 justify-content-center align-content-center p-0 shadow";
    overlay.style.display = 'block';
}
btn2.onclick = function () {
    barbercompleted.classList = "d-flex barbernoti col-12 justify-content-center align-content-center p-0 shadow";
    complete.style.display = 'block';
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    barbernoti.classList = "barbernoti col-12 justify-content-center";
    overlay.style.display = 'none';
}
span2.onclick = function () {
    barbercompleted.classList = "barbernoti col-12 justify-content-center";
    complete.style.display = 'none';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target.id == 'outFrame') {
        barbernoti.classList = "barbernoti col-12 justify-content-center";
        overlay.style.display = 'none';
    } else if (event.target.id == 'outOfFrame') {
        complete.style.display = 'none';
        barbercompleted.classList = "barbernoti col-12 justify-content-center";

    }
}

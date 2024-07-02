console.log("levi is bad please get rid of him")

document.addEventListener('keydown', function(event) {
    if(event.keyCode == 37) {
        if(document.getElementsByClassName("back_button")){
            document.getElementsByClassName("back_button")[0].press
        }
        alert('Left was pressed');
    }
    else if(event.keyCode == 39) {
        alert('Right was pressed');
    }
});
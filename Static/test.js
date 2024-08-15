let path = window.location.pathname;
let fileName = path.substring(path.lastIndexOf('/') + 1);
if(fileName == "admin_login"){
    document.getElementById("update").addEventListener("change", change_update)
    document.getElementById("table").addEventListener("change", change_table)
}
function change_update() {
    let update = document.getElementById("update")
    console.log(update.value)
}
function change_table() {
    let update = document.getElementById("table")
    console.log(update.value)
}

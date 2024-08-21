let update = document.getElementById("update")
let table = document.getElementById("table");
let path = window.location.pathname;
let fileName = path.substring(path.lastIndexOf('/') + 1);
if(fileName == "admin_login"){
    document.getElementById("update").addEventListener("change", change_update);
    document.getElementById("table").addEventListener("change", change_table);
}
function change_update() {
    update = document.getElementById("update");
    console.log(update.value);
}
function change_table() {
    table = document.getElementById("table");
    console.log(table.value);
    update_labels()
}

const label_names = {
    weapon:["Weapon ID", "Weapon Name", "Main Weapon", "Sub Weapon", "Special Weapon", "Points for Special", "Introduced Version"],
    main:["Weapon ID", "Weapon Name", "Weapon Type", "Damage", "Range", "Attack Rate", "Ink Usage", "Speed While Shooting"],
    sub:["Weapon ID", "Weapon Name", "Damage", "Ink Consumption", "Tracking Duration", "Damage Duration"],
    special:["Weapon ID", "Weapon Name", "Damage", "Number of Attacks", "Duration"]
}

function update_labels() {
    let hi = document.getElementsByClassName(String(table.value + "-table"));
    let bye = document.getElementsByTagName("tr")
    for(let i = 1; i < bye.length; i ++){
        bye[i].style.display = "none"
    }
    for(let i = 0; i < hi.length; i ++){
        hi[i].style.display = "block"
    }
}
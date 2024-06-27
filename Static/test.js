console.log("Hello World!");

// for(let i = 0; i < 10; i++){
//     console.log(i);
// }

const button_log = () => {
    const button = document.getElementsByClassName("link");
    for(let i = 0; i < button.length; i++){
        button[i].addEventListener(("mouseenter"), () =>{
            console.log(button[i])
            console.log(button[i].style.color)
            button[i].style.width = "10px";
        });
    }
}

// let index = 0
// while(index < 10){
//     console.log(index);
//     index ++;
// }

button_log()
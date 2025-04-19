let tempNums = document.querySelector(".temp-nums")
let temp = document.querySelector(".temp")
if (tempNums.innerHTML >= 10 && tempNums <= 30){
    temp.style.color = "red"
}
else if(tempNums.innerHTML >= 0 && tempNums <= 9){
    temp.style.color = "yellow"
}
else{
    temp.style.color = "blue"
}
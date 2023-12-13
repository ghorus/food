var rs = document.getElementsByClassName("ratingStars")
Array.from(rs).forEach(rating => {
    var num = parseInt(rating.innerHTML)
    rating.innerHTML = ""
    for(i=0;i<num;i++){
        const star = document.createElement("img")
        star.src = "/static/post_pics/star.png"
        star.style.height = "25px"
        star.style.backgroundColor = "rgb(220,20,60)"
        star.style.borderRadius = "5px"
        star.style.padding = "5px"
        star.style.margin = "0px 10px 0px 0px"
        rating.appendChild(star)
    }
})

//updateDelete
const updateDelete = document.getElementsByClassName("updateDeleteContainer")
Array.from(updateDelete).forEach(menu => {
    menu.addEventListener("click",()=>{
        if(menu.offsetHeight==40){menu.style.height="100%"}
        else{menu.style.height="40px"}
    })
})
   
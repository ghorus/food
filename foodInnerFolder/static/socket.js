//socket home likes
var socket = io();
const likeButton = document.getElementsByClassName("likeButton")
const totalLikes = document.getElementsByClassName("totalLikes")
Array.from(likeButton).forEach(like => {
        $(like).unbind('click').click(function(){
        socket.emit('like',like.id)
        socket.on('like',(data)=>{
            like.nextElementSibling.innerHTML = data + " Likes"
        })
})
})
socket.on('redirect', (dest) => {
    window.location.href = dest;
    });

//creategames
socket.on('create a game',(data)=>{
    console.log(data)
})
function createGame(){
    socket.emit('create a game')
}
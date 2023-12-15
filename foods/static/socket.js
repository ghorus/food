//socket home likes
var socket = io();
const likeButton = document.getElementsByClassName("likeButton")
const totalLikes = document.getElementsByClassName("totalLikes")
Array.from(likeButton).forEach(like => {
        $(like).unbind('click').click(function(){
        socket.emit('like',like.id)
        socket.on('like',(data)=>{
            like.nextElementSibling.innerHTML = data + " Likes"
            like.style.animation = "newLike 0.3s"
        })
})
})
socket.on('redirect', (dest) => {
    window.location.href = dest;
    });

//game messaging
const flash_message = document.querySelector(".flashMessage")
const gameMessage = document.querySelector(".gameMessage")
const messagesContainer = document.querySelector(".messagesContainer")
const roomLink = document.querySelector('.roomLink')
const submit = document.querySelector(".gameMessageSubmit")
// submit.addEventListener('click',()=>{
//     socket.emit('send game message',({message:gameMessage.value,link:roomLink.innerHTML}))
//     gameMessage.value=""
// })
// socket.on('send game message',(words)=>{
//     messagesContainer.innerHTML = ""
//     for(i=0;i<words.length;i++){
//         messagesContainer.innerHTML = messagesContainer.innerHTML + words[i] + " "
//     }
// })
// socket.on('flashy',(data)=>{
//     flash_message.innerHTML = data
// })


// //total users
// socket.on('total users',data=>{
//     const displayTotalUsers = document.querySelector(".totalUsers")
//     displayTotalUsers.innerHTML = data + " current users total!"
// })
// const displayTotalUsers = document.querySelector(".totalUsers")
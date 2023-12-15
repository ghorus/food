//socket home likes
var socket = io();
var likes = io('/likes')
const likeButton = document.getElementsByClassName("likeButton")
const totalLikes = document.getElementsByClassName("totalLikes")
Array.from(likeButton).forEach(like => {
        $(like).unbind('click').click(function(){
        likes.emit('like',like.id)
        likes.on('like',(data)=>{
            like.nextElementSibling.innerHTML = data + " Likes"
            like.style.animation = "newLike 0.3s"
        })
})
})
socket.on('redirect', (dest) => {
    window.location.href = dest;
});
//total users
socket.on('total users',data=>{
    const displayTotalUsers = document.querySelector(".totalUsers")
    displayTotalUsers.innerHTML = data + " current users total!"
    displayTotalUsers.classList.remove('totalUsersAnimation');
    setTimeout(function(){
        displayTotalUsers.classList.add('totalUsersAnimation');
    },10);
})
// // // game messaging
// var messaging = io('/messaging')
// const flash_message = document.querySelector(".flashMessage")
// const gameMessage = document.querySelector(".gameMessage")
// const messagesContainer = document.querySelector(".messagesContainer")
// const roomLink = document.querySelector(".roomLink")
// const submit = document.querySelector(".gameMessageSubmit")
// submit.addEventListener('click',()=>{
//     socket.emit('send game message',({message:gameMessage.value,link:roomLink.innerHTML}))
//     gameMessage.value=""
// })
// messaging.on('send game message',(words)=>{
//     messagesContainer.innerHTML = ""
//     for(i=0;i<words.length;i++){
//         messagesContainer.innerHTML = messagesContainer.innerHTML + words[i] + " "
//     }
// })
// messaging.on('flashy',(data)=>{
//     flash_message.innerHTML = data
//     flash_message.classList.remove('totalUsersAnimation');
//     setTimeout(function(){
//         flash_message.classList.add('totalUsersAnimation');
//     },10);
// })

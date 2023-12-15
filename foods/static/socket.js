//socket home likes
var socket = io();
var likes = io('https://food-v6q5.onrender.com/likes')
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
likes.on('redirect', (dest) => {
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
// game messaging
var messaging = io('https://food-v6q5.onrender.com/messaging')
const flash_message = document.querySelector(".flashMessage")
const gameMessage = document.querySelector(".gameMessage")
const messagesContainer = document.querySelector(".messagesContainer")
const roomLink = document.querySelector(".roomLink")
const submit = document.querySelector(".gameMessageSubmit")
submit.addEventListener('click',()=>{
    messaging.emit('send game message',({message:gameMessage.value,link:roomLink.innerHTML}))
    gameMessage.value=""
})
messaging.on('send game message',(words)=>{
    messagesContainer.innerHTML = ""
    for(i=0;i<words.length;i++){
        messagesContainer.innerHTML = messagesContainer.innerHTML + words[i] + " "
    }
})
messaging.on('flashy',(data)=>{
    flash_message.innerHTML = data
    flash_message.classList.remove('totalUsersAnimation');
    setTimeout(function(){
        flash_message.classList.add('totalUsersAnimation');
    },10);
})

//join room
var join = io('https://food-v6q5.onrender.com/join')
join.on('connect',()=>{if(roomLink != null){
    join.emit('join',roomLink.innerHTML);
}})
join.on('message',data=>{
    console.log(data + 'hi')})

//postAdlib
var posting = io('https://food-v6q5.onrender.com/posting')
function postAdlib(){
    const allAdlibs = messagesContainer.innerHTML
    const allMembers = document.querySelectorAll(".memberIds")
    const roomTitle = document.querySelector(".roomTitle").innerHTML
    var totalMembers = ""
    for(i=0;i<allMembers.length;i++){
        totalMembers += allMembers[i].innerHTML
    }
    console.log(totalMembers)
    var data={adlibs:allAdlibs,
        members:totalMembers,
        roomTitle:roomTitle,
        room_link:roomLink.innerHTML}
    posting.emit('post adlib',data)
}
posting.on('redirect', (dest) => {
    window.location.href = dest;
});
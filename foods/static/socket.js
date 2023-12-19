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

//adlib likes
var adliblikes = io('https://food-v6q5.onrender.com/adliblikes')
const adlibLikeButton = document.getElementsByClassName("adlibLikeButton")
const adlibTotalLikes = document.getElementsByClassName("adlibTotalLikes")
Array.from(adlibLikeButton).forEach(like => {
        $(like).unbind('click').click(function(){
        adliblikes.emit('adlib like',like.id)
        adliblikes.on('adlib like',(data)=>{
            like.nextElementSibling.innerHTML = data + " Likes"
            like.style.animation = "newLike 0.3s"
        })
})
})
adliblikes.on('redirect', (dest) => {
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
//game message press enter
gameMessage.addEventListener("keypress",(e)=>{
    if(e.key=='Enter'){
        messaging.emit('send game message',({message:gameMessage.value,link:roomLink.innerHTML}))
        gameMessage.value=""
    }
})
//join room
messaging.on('connect',()=>{if(roomLink != null){
    const allMembers = document.querySelectorAll(".memberIds")
    var totalMembers = ""
    for(i=0;i<allMembers.length;i++){
        totalMembers += allMembers[i].innerHTML
    }
    var data = {roomLink:roomLink.innerHTML}
    messaging.emit('join',data);
}})
//leaving game room
function leaving (){
    var data = {roomLink:roomLink.innerHTML}
    messaging.emit('dc',data)
}
messaging.on('redirect', (dest) => {
    window.location.href = dest;
});

const turn_message = document.querySelector(".turnMessage")
//game member's turn 
messaging.on('turn',(data)=>{
    turn_message.innerHTML = data
    turn_message.classList.remove('totalUsersAnimation');
    setTimeout(function(){
        turn_message.classList.add('totalUsersAnimation');
    },10);
})


messaging.on('flashy',(data)=>{
    flash_message.innerHTML = data
    flash_message.classList.remove('totalUsersAnimation');
    setTimeout(function(){
        flash_message.classList.add('totalUsersAnimation');
    },10);
})

messaging.on('members',(data)=>{
    const memberContainer = document.querySelector(".memberContainer")
    memberContainer.innerHTML=""
    for(i=0;i<data.length;i++){
        const memb = document.createElement("span")
        memb.classList.add("member")
        memb.innerHTML+=data[i]
        memberContainer.appendChild(memb)
    }
})

messaging.on('send game message',(words)=>{
    messagesContainer.innerHTML = ""
    for(i=0;i<words.length;i++){
        messagesContainer.innerHTML = messagesContainer.innerHTML + words[i] + " "
    }
})

//postAdlib
var posting = io('https://food-v6q5.onrender.com/posting')
function postAdlib(){
    const allAdlibs = messagesContainer.innerHTML
    const allMembers = document.querySelectorAll(".memberIds")
    var roomTitle = document.querySelector(".roomTitle").innerHTML
    var totalMembers = ""
    for(i=0;i<allMembers.length;i++){
        totalMembers += allMembers[i].innerHTML
    }
    var data={adlibs:allAdlibs,
        members:totalMembers,
        roomTitle:roomTitle,
        room_link:roomLink.innerHTML}
    posting.emit('post adlib',data)
}
posting.on('redirect', (dest) => {
    window.location.href = dest;
});
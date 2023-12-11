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


const myVideo = document.createElement("video")
var peer = new Peer();
const peers = {}
const videoGrid = document.getElementById("video-grid")
myVideo.muted=true
const host = document.querySelector(".host")
const viewer = document.querySelector(".viewer")
var i = []
navigator.mediaDevices.getUserMedia({
    video:true,
    audio: {
        echoCancellation: false,
        autoGainControl: false,
        noiseCancellation: false
    }
}).then(stream => {
    if (host==viewer){
        addVidStream(myVideo,stream)
    }
    peer.on('call',call =>{
        call.answer(stream)
        const vid = document.createElement('video')
        call.on('stream',otherGuysStream =>{
            i.push(otherGuysStream.id)
            if(otherGuysStream.id != i[0])
                addVidStream(vid,otherGuysStream)
        })
    })
    socket.on('listen to new users',(id)=>{
        connectNewGuy(id,stream)
    })

    
})
peer.on('open', id => {
    socket.emit('listen to new users',id)
});

function addVidStream(video,stream){
video.srcObject = stream
video.addEventListener('loadedmetadata',()=>{
    video.play()
})
videoGrid.append(video)
}
function connectNewGuy(id,stream){
    const call = peer.call(id,stream)
    const vid = document.createElement('video')
    call.on('stream',remoteStream =>{
        addVidStream(vid,remoteStream)
    })
    call.on('close',()=>{
        vid.remove()
    })
}

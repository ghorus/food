const myVideo = document.createElement("video")
var peer = new Peer();
var socket = io()
const videoGrid = document.getElementById("video-grid")
myVideo.muted=true

const streamer = document.querySelector(".host").innerHTML
const viewer = document.querySelector(".viewer").innerHTML
if(streamer==viewer){
    navigator.mediaDevices.getUserMedia({
        video:true,
        audio: {
            echoCancellation: false,
            autoGainControl: false,
            noiseCancellation: false
        }
    }).then(stream => {
        addVidStream(myVideo,stream)
        socket.on('listen to new users',(id)=>{
            console.log(id)
        })
        peer.on('open', id => {
            socket.emit('listen to new users',id)
            });
    })
        
    function addVidStream(video,stream){
        video.srcObject = stream
        video.addEventListener('loadedmetadata',()=>{
            video.play()
        })
        videoGrid.append(video)
        }
}

//socket home likes
var socket = io();
    const likeButton = document.getElementsByClassName("likeButton")
    const totalLikes = document.getElementsByClassName("totalLikes")
    Array.from(likeButton).forEach(like => {
            $(like).unbind('click').click(function(){
            socket.on('like',(data)=>{
                like.nextElementSibling.innerHTML = data + " Likes"
            })
            socket.emit('like',like.id)
    })
    })
    socket.on('redirect', (dest) => {
        window.location.href = dest;
        });

//streaming
// const myVideo = document.createElement("video")
// var peer = new Peer();
// const videoGrid = document.getElementById("video-grid")
// myVideo.muted=true

// const streamer = document.querySelector(".host").innerHTML
// const viewer = document.querySelector(".viewer").innerHTML
// if(streamer==viewer){
//     navigator.mediaDevices.getUserMedia({
//         video:true,
//         audio: {
//             echoCancellation: false,
//             autoGainControl: false,
//             noiseCancellation: false
//         }
//     }).then(stream => {
//         addVidStream(myVideo,stream)
//         socket.on('listen to new users',(id)=>{
//             console.log(id)
//             connectToNewUser(id,stream)
//             function connectToNewUser(id,stream){
//                 const call = peer.call(id,stream)
//                 //     const vid = document.createElement('video')
//                 call.on('stream',userVidStream=>{
//                     // addVidStream(vid,userVidStream)
//                     console.log('calling ' + id, userVidStream)
//                 })
//                 //     call.on('close',()=>{
//                 //         vid.remove()
//                 //         console.log('user left')
//                 //     })
//             }
//         })
//         peer.on('open', id => {
//             socket.emit('listen to new users',id)
//             });
//     })
        
//     function addVidStream(video,stream){
//         video.srcObject = stream
//         video.addEventListener('loadedmetadata',()=>{
//             video.play()
//         })
//         videoGrid.append(video)
//         }
// }
     
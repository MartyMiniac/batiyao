var socket = io.connect('http://' + document.domain + ':' + location.port);
var friendinfo=[];

$("#addfriendbutton").click(function(event){
    event.preventDefault();
    socket.emit('Add Friend',{
        data: document.getElementById("iptextid").value
    })
})

socket.on('Add Friend Response', (data) => {
    if(data.found){
        let s=""
        s+="<div class=\"connectionpaneflexitem\" id=\"ip"+data.ip+"\" value=\""+data.ip+"\">";
        s+="<h4>"+data.nickname+"</h4>";
        s+="</div>";
        $("#connectionlist").append(s);
        friendinfo.push(data);
    }
  });

socket.on('Different Login', (data) => {
    window.location.replace("/");
});

socket.on('Message Received', (data) => {
    console.log(data);
});
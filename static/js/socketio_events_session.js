var socket = io.connect('http://' + document.domain + ':' + location.port);


$("#addfriendbutton").click(function(event){
    event.preventDefault();
    socket.emit('Add Friend',{
        data: document.getElementById("iptextid").value
    })
})

socket.on('Add Friend Response', (data) => {
    console.log(data);
    if(data.found){
        let s=""
        s+="<div class=\"connectionpaneflexitem\" id=\"ip"+data.ip+"\">";
        s+="<h4>"+data.nickname+"</h4>";
        s+="</div>";
        $("#connectionlist").append(s);
    }
  });
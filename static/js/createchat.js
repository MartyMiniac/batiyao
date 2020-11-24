$(document).on('click','.connectionpaneflexitem',function(event){
    let ip=$(this).attr('value');
    for(let i=0; i<friendinfo.length; i++){
        val=friendinfo[i];
        if(val.ip==ip) {
            if(bodydisplay.chatfriendbool && document.getElementById("chatfriendname").innerHTML==val.nickname){
                document.getElementById("friendchatid").style.visibility="hidden";
                bodydisplay.chatfriendbool=false;
                break;
            }      
            document.getElementById("chatfriendname").innerHTML=val.nickname;
            document.getElementById("friendchatid").style.visibility="visible";
            bodydisplay.chatfriendbool=true;
            break;
        }
    };
});
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
function getip(nickname){
    for(let i=0; i<friendinfo.length; i++){
        val=friendinfo[i];
        if(val.nickname==nickname)
        return val.ip;
    }
}
$("#sendmsgbutton").click(function(){
    let t=document.getElementById("chatfriendname").innerHTML;
    t='http://'+getip(t)+'/api/sendmsg';

    let xhr = new XMLHttpRequest();

    // open a connection 
    xhr.open("POST", t, true);
    xhr.setRequestHeader("Content-Type", "application/json"); 

    // Create a state change callback 
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status === 200) {
        }
    };
    var data = JSON.stringify({ "name": getCookie("name"), "nickname": getCookie("nickname"), "ip": location.hostname, "msg": document.getElementById("messageboxid").value }); 

    // Sending data with the request 
    xhr.send(data); 
});
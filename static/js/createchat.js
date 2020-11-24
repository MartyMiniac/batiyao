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
            if (val.nickname in chatdb)
                document.getElementById("chatboxid").innerHTML=chatdb[val.nickname];
            else
                document.getElementById("chatboxid").innerHTML="";
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
function updatesendbox(msg){
    let s="";
    let m="";
    for(let i=0; i<msg.length; i++){
        if(msg.charAt(i)=='\n'){
            m+="<br>";
            continue;
        }
        m+=msg.charAt(i);
    }
    m="<strong>You said :</strong><br>"+m;
    s+="<div class=\"chatbubble\">";
    s+=m;
    s+="</div>";
    if (document.getElementById("chatfriendname").innerHTML in chatdb)
        chatdb[document.getElementById("chatfriendname").innerHTML]+=s;
    else        
        chatdb[document.getElementById("chatfriendname").innerHTML]=s;
    $(".chatbox").append(s);
}
function updaterecievebox(msg,nickname){
    let s="";
    let m="";
    for(let i=0; i<msg.length; i++){
        if(msg.charAt(i)=='\n'){
            m+="<br>";
            continue;
        }
        m+=msg.charAt(i);
    }
    m="<strong>"+nickname+" said :</strong><br>"+m;
    s+="<div class=\"chatbubble\">";
    s+=m;
    s+="</div>";
    if (nickname in chatdb)
        chatdb[nickname]+=s;
    else
        chatdb[nickname]=s;
    if(document.getElementById("chatfriendname").innerHTML==nickname)
        $(".chatbox").append(s);
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
    updatesendbox(document.getElementById("messageboxid").value);
    document.getElementById("messageboxid").value="";
});
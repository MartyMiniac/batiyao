$("#addbutton").click(function(){
    if(bodydisplay.addfriendbool){
        document.getElementById("addfrienddivid").style.visibility="hidden";
        bodydisplay.addfriendbool=false;
        document.getElementById("iptextid").value="";
    }
    else{
        document.getElementById("addfrienddivid").style.visibility="visible";
        bodydisplay.addfriendbool=true;
    }
})
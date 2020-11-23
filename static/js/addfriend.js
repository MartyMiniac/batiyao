var addfriendbool=false;
$("#addbutton").click(function(){
    if(addfriendbool){
        document.getElementById("addfrienddivid").style.visibility="hidden";
        addfriendbool=false;
    }
    else{
        document.getElementById("addfrienddivid").style.visibility="visible";
        addfriendbool=true;
    }
})
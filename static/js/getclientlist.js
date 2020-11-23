function getclientlist(){
    $.getJSON( "api/getuserlist", function( data ) {
        let s="";
        $.each( data, function( key, val ) {
            s+="<div class=\"connectionpaneflexitem\">";
            s+="<h4>"+val.ip+"</h4>";
            s+="</div>";
            document.getElementById("connectionlist").innerHTML=s;
        });
      });
}
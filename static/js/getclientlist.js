function getclientlist(){
    $.getJSON( "api/getuserlist", function( data ) {
        let s="";
        $.each( data, function( key, val ) {
            s+="<div class=\"connectionpaneflexitem\" id=\"ip"+val.ip+"\" value=\""+val.ip+"\">";
            s+="<h4>"+val.nickname+"</h4>";
            s+="</div>";
            friendinfo.push(val);
        });
        document.getElementById("connectionlist").innerHTML=s;
      });
}
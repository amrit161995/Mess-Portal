
$( document ).ready(function() {
    $("#If").attr('src',"Home_Content.html");
        $("#li_Menu").attr('class',"");
         $("#li_Home").attr('class',"active");
          $("#li_Contact").attr('class',"");
           $("#li_Team").attr('class',"");
            $("#li_Logout").attr('class',"");
             $("#li_Bill").attr('class',"");
});

	$(function(){
    $("#aMenu").click(function(e){
        e.preventDefault(); //To prevent the default anchor tag behaviour
       
        $("#If").attr('src',"Menu.html");
        $("#li_Menu").attr('class',"active");
         $("#li_Home").attr('class',"");
          $("#li_Contact").attr('class',"");
           $("#li_Team").attr('class',"");
            $("#li_Logout").attr('class',"");
             $("#li_Bill").attr('class',"");
    });
});


$(function(){
    $("#aTeam").click(function(e){
        e.preventDefault(); //To prevent the default anchor tag behaviour
       
        $("#If").attr('src',"Team.html");
        $("#li_Menu").attr('class',"");
         $("#li_Home").attr('class',"");
          $("#li_Contact").attr('class',"");
           $("#li_Team").attr('class',"active");
            $("#li_Logout").attr('class',"");
             $("#li_Bill").attr('class',"");
    });
});

$(function(){
    $("#aHome").click(function(e){
        e.preventDefault(); //To prevent the default anchor tag behaviour
       
        $("#If").attr('src',"Home_Content.html");
        $("#li_Menu").attr('class',"");
         $("#li_Home").attr('class',"active");
          $("#li_Contact").attr('class',"");
           $("#li_Team").attr('class',"");
            $("#li_Logout").attr('class',"");
             $("#li_Bill").attr('class',"");
    });
});

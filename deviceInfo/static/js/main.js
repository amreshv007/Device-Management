$(document).ready(function(){
    $("#takenfrom").hide();
    $('#a').css('background', '#d25252');
    $('#a').css('color', 'white'); 
    $("#a").click(function(){
        $("#takenfrom").hide();
        $("#givento").show();
        $('#a').css('background', '#d25252');
        $('#a').css('color', 'white'); 
        $('#b').css('background', '#b3b2b25e');
        $('#b').css('color', 'black'); 
    });

    $("#b").click(function(){
        $("#givento").hide();
        $("#takenfrom").show();
        $('#b').css('background', '#d25252');
        $('#b').css('color', 'white'); 
        $('#a').css('background', '#b3b2b25e');
        $('#a').css('color', 'black'); 
    });
});
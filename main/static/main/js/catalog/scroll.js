$(document).ready(function () {
    $("#nav-competitions").click(function(){
        $('html, body').animate({
                scrollTop: $("#competitions").offset().top
            }, 500);
    });
    $("#nav-practice").click(function(){
        $('html, body').animate({
                scrollTop: $("#practice").offset().top
            }, 500);
    });
    $("#nav-workshops").click(function(){
        $('html, body').animate({
                scrollTop: $("#workshops").offset().top
            }, 500);
    });
    $("#nav-classes").click(function(){
        $('html, body').animate({
                scrollTop: $("#classes").offset().top
            }, 500);
    });
});
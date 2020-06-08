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

$(document).ready(function(){
	$(window).scroll(function () {
			if ($(this).scrollTop() > 50) {
				$('#back-to-top').fadeIn();
			} else {
				$('#back-to-top').fadeOut();
			}
		});
		// scroll body to 0px on click
		$('#back-to-top').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 400);
			return false;
		});
});
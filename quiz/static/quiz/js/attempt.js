// Adds a confirm dialog before page unload
function stopPageExit() {
    if (confirm("Are you sure you want to leave without submitting?")) {
        window.close();
    }
}

$(window).on('beforeunload', function(){
  return stopPageExit;
});

// utility functions

function isEmpty(obj) {
    for(let key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

function scrollToAnchor(aid){
    $('html,body').animate({scrollTop: $('#' + aid).offset().top},'slow');
}

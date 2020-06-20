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

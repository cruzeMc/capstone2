$(document).ready(function(){
    var tocWrapperHeight = 260;
    var tocHeight = $('#sticky').length ? $('#bar').height() : 0;
    var footerOffset = $('body > footer').first().length ? $('body > footer').first().offset().top : 0;
    var barHeight = $('#bar').length ? $('#bar').height() : 0;
    var topNavHeight = $('#top-nav').height();
    var barOffset = barHeight + $('#bar').offset().top;
    var bottomOffset = footerOffset - barOffset - tocWrapperHeight;
    var topOffset = barOffset+topNavHeight
    $('#sticky').pushpin({bottom:bottomOffset, top:topOffset});
 });
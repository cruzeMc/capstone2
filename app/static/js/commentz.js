$(function() {
  $('button#upost').bind('click', function() {
    $.ajax({
    type: "GET",
      url: $SCRIPT_ROOT + "/comment_recieved",
      data: {
        'c': $('input[name="c"]').val()
        },
        success: commentSuccess,
        dataType: 'html'
    });
  });
});
function commentSuccess(data, textStatus, jqXHR)
{
  $('#comment_results').html(data);
  $('.comment_box').animate({
        scrollTop: $(".comment_box").offset().bottom-65},
        'slow');
}
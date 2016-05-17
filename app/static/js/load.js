$(function() {
  $(document).ready(function() {
    $.ajax({
    type: "GET",
      url: $SCRIPT_ROOT + "/comment_recieved",
      data: {
        'c': $('input[name="c"]').val()
        },
        success: loadSuccess,
        dataType: 'html'
    });
  });
});
function loadSuccess(data, textStatus, jqXHR)
{
  $('#comment_results').html(data);
}
$(function() {
  $(document).ready(function() {
    $.ajax({
    type: "GET",
      url: $SCRIPT_ROOT + "/page_count",
      data: {
        'c': $('input[name="c"]').val()
        },
        success: hitsSuccess,
        dataType: 'html'
    });
  });
});
function hitsSuccess(data, textStatus, jqXHR)
{
  $('#hits').html(data);
}
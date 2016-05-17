$(function() {
  $('button#upost').bind('click', function() {
    Materialize.toast('You posted' + " " +  $('textarea[name="b"]').val(), 3000, 'rounded');
    $.getJSON($SCRIPT_ROOT + '/comment_sent', {
      a: $('input[name="a"]').val(),
      b: $('textarea[name="b"]').val(),
      c: $('input[name="c"]').val(),
      d: $('input[name="d"]').val()
    }, function(data) {
      $("#cPost").val("");
    });
    return false;
  });
});
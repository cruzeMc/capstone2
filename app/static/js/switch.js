$(function() {
  $('input:checkbox').change(function() { 
    $.ajax({
    type: "GET",
      url: $SCRIPT_ROOT + "/switch",
      dataType: 'html',
      data: {
        'c': $(this).attr("value"),
        'u': $('#user_id').attr('value')
        },
        beforeSend: function()
        {
          if($("input:checkbox").is(":checked") ? 1:0){ 
            Materialize.toast('You are switching to Promoter', 3000, 'rounded');
          }
          else{
            Materialize.toast('You are switching to User', 3000, 'rounded');
          }
        },
        complete: function()
        {
            Materialize.toast('Account Switched', 3000, 'rounded');
        },
        success: function(data){
          Materialize.toast('You are now a ' + data, 3000, 'rounded');
        }
    });
  });
});
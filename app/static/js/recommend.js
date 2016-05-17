$(function() {
  $(document).ready(function() {
    $.ajax({
    type: "GET",
      url: $SCRIPT_ROOT + "/recommendations",
      beforeSend: function() {
              $("#loadingDiv").css("display","block");  
            },
      complete: function() {
              $("#loadingDiv").css("display","none");  
            },
        success: recommendSuccess,
        dataType: 'html'
    });
  });
});
function recommendSuccess(data, textStatus, jqXHR)
{
  $('#recommend').html(data);
}

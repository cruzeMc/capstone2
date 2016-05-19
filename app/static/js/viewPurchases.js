$(function() {
  $('button#viewPurchases').bind('click', function() {
    $.ajax({
    type: "GET",
      url: $SCRIPT_ROOT + "/event_list",
      dataType: 'html',
      data: {
        'c': $(this).attr("value")
        },
        beforeSend: function()
        {
            $("#loader").show();
          if($("#statistics")){
            $("#statistics").css("opacity",0.6).fadeIn(300, function () {
                //Attempting to set/make #red appear upon the dimmed DIV
                $('#red').css('zIndex', 10000);
            });
            }
            else {
            $("#what_if_analysis").css("opacity",0.6).fadeIn(300, function () {
                //Attempting to set/make #red appear upon the dimmed DIV
                $('#red').css('zIndex', 10000);
            });
          }
        },
        complete: function()
        {
              $("#loader").hide();
              if($("#statistics")){
                  $("#statistics").css("opacity",1.0).fadeIn(300, function () {
                //Attempting to set/make #red appear upon the dimmed DIV
                  $('#red').css('zIndex', 10000);
                });
              }
              else{
                  $("#what_if_analysis").css("opacity",1.0).fadeIn(300, function () {
                //Attempting to set/make #red appear upon the dimmed DIV
                  $('#red').css('zIndex', 10000);
                });
              }
                $('#pic').hide();
                $('#what_if_analysis').hide();
                $('#editEvents').hide();
                $('#viewPurchase').show();
                $('#statistics').hide();
        },
        success: function(data){
          $('#statistics').html(data);
        }
    });
  });
});
$(function() {
  $('button#editEvent').bind('click', function() {
    $.ajax({
    type: "GET",
      url: $SCRIPT_ROOT + "/update_event",
      dataType: 'html',
      data: {
        'c': $(this).attr("value")
        },
        beforeSend: function()
        {
            $("#loader").show();
            $("#statistics").css("opacity",0.6).fadeIn(300, function () {
                //Attempting to set/make #red appear upon the dimmed DIV
                $('#red').css('zIndex', 10000);
            });
        },
        complete: function()
        {
              $("#loader").hide();
              $('#pic').hide();
              $('#what_if_analysis').hide();
              $('#viewPurchase').hide();
              $('#statistics').hide();
              $('#editEvents').show
        },
        success: function(data){
          $('#editEvents').html(data);
        }
    });
  });
});
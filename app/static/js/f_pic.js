$(function(){
   $('#username').change(function(){
     $.ajax({
       type: "POST",
       url: "/usersearch",
       data: {
           'search_text' : $('#username').val(),
     },
       success: picSuccess,
       dataType: 'html'
   });
  });
});
function picSuccess(data, textStatus, jqXHR)
{
    $('#p_image').hide();
    $('#f_image').html('<img src="/static/profile_pics/' + data + '" />');
}
$(function() {
      $('a#calculate').bind('click', function() {
        $.getJSON('/login', {
          username: $('input[name="username"]').val(),
          password: $('input[name="password"]').val()
        }, function(data) {
          $("#Err").text(data.result);
        });
        return false;
      });
    });
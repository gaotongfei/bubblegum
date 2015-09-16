$(document).ready(function() {
    $('.message').each(function() {
        $(this).on("click", function() {
            $.getJSON('/message_is_read', {
                is_read: 1,
                message_id: $(this).attr("id")
            }, function(data){
                console.log(data);
            });
        });
    });
    $('#upvote').on('click', function() {
      var href = window.location.href;
      var lastSegment = href.split('/').pop()
      var lastChar = lastSegment.substr(lastSegment.length-1)
      if (lastChar == '#') {
        lastSegment = lastSegment.slice(0, -1)
        alert(lastSegment)
      }
    })
});

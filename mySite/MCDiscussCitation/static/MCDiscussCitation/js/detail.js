// This function requires a browser that supports HTML5
function ChangeUrl(title, url) {
    if (typeof (history.pushState) != "undefined") {
        var obj = { Title: title, Url: url };
        history.pushState(obj, obj.Title, obj.Url);
    } else {
        alert("Please use a modern browser that supports HTML5 (like Google Chrome)");
    }
}


$(document).ready(function() {
  // create hyperlinks to all images in posts
  $('.post-wrapper img').each(function(index) {
    var img = $(this)
    img.wrap( "<a href='" + img.attr("src") + "'></a>" );
  });

  // Highlight url target
  if(window.location.hash) {
    var url = window.location.href
    var focused_div = url.substring(url.indexOf("#")+1)
    $('#'+focused_div).addClass("background-color-yellow")
  }

  // Change url when different tabs
  $( ".thread-switch-button" ).click(function(event){
    // this changes url to reflect new thread without reloading
    var threadnumber = $(this).attr("data-threadnumber")
    ChangeUrl("","../"+threadnumber+"/")

    // this changes social authentication redirect to go to new thread
    $('.social-login-link').each(function(index) {
      var link = $(this)
      var original_href = link.attr('href')
      var arr = original_href.split('/');
      var reconstructed_str = ''
      $.each(arr, function( index, value ) {
        // this is the equivalent of continue if value==''
        if (value == '') {
          return
        }
        // this is the equivalent of break if index exceeds limit
        if (index > arr.length-3 ) {
          return false
        }
        reconstructed_str += '/' + value
      });
      reconstructed_str += '/' + threadnumber + '/'
      link.attr('href',reconstructed_str)
    });

    // this changes reply/edit/comment links to go to new thead
    $('.editor-redirect-url').each(function(index) {
      var input = $(this)
      var original_href = input.attr('value')
      var arr = original_href.split('/');
      var reconstructed_str = ''
      $.each(arr, function( index, value ) {
        // this is the equivalent of continue if value==''
        if (value == '') {
          return
        }
        // this is the equivalent of break if index exceeds limit
        if (index > arr.length-3 ) {
          return false
        }
        reconstructed_str += '/' + value
      });
      reconstructed_str += '/' + threadnumber + '/'
      input.attr('value',reconstructed_str)
    });


  });



});

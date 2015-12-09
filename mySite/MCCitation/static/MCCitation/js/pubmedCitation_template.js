base_namespace.pubmedCitation_template = base_namespace.pubmedCitation_template || {};

$(document).ready(function() {
  // make sure this javascript file is only loaded once
  if (!isFirstLoad(base_namespace.pubmedCitation_template)) {
    return;
  }

  // hide all other citations when one is clicked.
  $( "a[id*='citation-toggle-']" ).click(function(e) {
    $('.citation-index-all').collapse('hide');
  });

  // import button functionality
  $(".import-citation").click(function() {
    var b = $( this )
    var f = b.next('form');
    var url = f.attr( 'action' );
    if ( b.hasClass('import-citation')) { // this is required because click doesn't detect changes to class
      $.ajax({
        type: "POST",
        url: url,
        data: f.serialize(),
        success: function(data) {
          b.removeClass('import-citation')
          b.parent().attr("href",data)
          b.html("Click to discuss this paper!")
        }
      });
    }
  });

});

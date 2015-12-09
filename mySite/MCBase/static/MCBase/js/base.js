var base_namespace = base_namespace || {};

var isFirstLoad = function(namespace) {
  var isFirst = namespace.firstLoad == undefined;
  namespace.firstLoad = false;
  if (!isFirst) {
    console.log('javascript file was included more than once')
  }
  return isFirst;
}

$(document).ready(function() {
  // submit next form when a hyperlink with class '' is clicked
  $("a.submit-next-form").click(function() {
    $( this ).next('form').submit();
  });
});

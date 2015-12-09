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
});

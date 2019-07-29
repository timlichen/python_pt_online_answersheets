$(document).ready(function() {
  // determine if a color was supplied by evaluating pathname
  var pathname = window.location.pathname;
  pathParts = pathname.split('/');
  if (pathParts.length > 3) {
    // this means colors were added in path
    var c1 = pathParts[3];
    var c2 = pathParts[4];
    $('.color1').css('background-color', c1);
    $('.color2').css('background-color', c2);
  }
});

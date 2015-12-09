base_namespace.display_single_post_template = base_namespace.display_single_post_template || {};

$(document).ready(function() {

  // make sure this javascript file is only loaded once
  if (!isFirstLoad(base_namespace.display_single_post_template)) {
    return;
  }

  // upvote button functionality
  $( ".upvote-button " ).click(function() {
    var me = $( this )
    var url = me.attr( 'url' );
    var post_pk = me.attr( 'postpk' )
    if ( me.hasClass('vote-toggle-off') )  {
      $.ajax({
           type:"GET",
           url: url,
           success: function(data){
             me.addClass('vote-toggle-on').removeClass('vote-toggle-off');
             $( "#down-"+post_pk ).addClass('vote-toggle-off').removeClass('vote-toggle-on');
             $( "#commentscore-pk-"+post_pk ).html( data )
             me.html( 'upvoted' )
             $( "#down-"+post_pk ).html( 'downvote' )
           }
      });
    } else if ( me.hasClass('vote-toggle-on') ) {
      $.ajax({
        type:"GET",
        url: url,
        success: function(data){
          me.addClass('vote-toggle-off').removeClass('vote-toggle-on');
          $( "#commentscore-pk-"+post_pk ).html( data )
          me.html( 'upvote' )
        }
      });
    }
  });

  // downvote button functionality
  $( ".downvote-button " ).click(function() {
    var me = $( this )
    var url = me.attr( 'url' );
    var post_pk = me.attr( 'postpk' )
    if ( me.hasClass('vote-toggle-off') )  {
      $.ajax({
           type:"GET",
           url: url,
           success: function(data){
             me.addClass('vote-toggle-on').removeClass('vote-toggle-off');
             $( "#up-"+post_pk ).addClass('vote-toggle-off').removeClass('vote-toggle-on');
             $( "#commentscore-pk-"+post_pk ).html( data )
             me.html( 'downvoted' )
             $( "#up-"+post_pk ).html( 'upvote' )
           }
      });
    } else if ( me.hasClass('vote-toggle-on') ) {
      $.ajax({
           type:"GET",
           url: url,
           success: function(data){
             me.addClass('vote-toggle-off').removeClass('vote-toggle-on');
             $( "#commentscore-pk-"+post_pk ).html( data )
             me.html( 'downvote' )
           }
      });
    }
  });


});

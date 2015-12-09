base_namespace.display_single_post_template = base_namespace.display_single_post_template || {};

$(document).ready(function() {

  // make sure this javascript file is only loaded once
  if (!isFirstLoad(base_namespace.display_single_post_template)) {
    return;
  }

  $( ".upvote-button " ).click(function() {
    var me = $( this )
    var url = me.attr( 'url' );
    var post_pk = me.attr( 'postpk' )
    if ( me.hasClass('up-arrow') )  {
      $.ajax({
           type:"GET",
           url: url,
           success: function(data){
             $( me ).addClass('upvoted-arrow').removeClass('up-arrow').addClass('active-vote');
             $( "#down-"+post_pk ).addClass('down-arrow').removeClass('downvoted-arrow').removeClass('active-vote');
             $( "#commentscore-pk-"+post_pk ).html( data )
             $( "#up-"+post_pk ).html( 'upvoted' )
             $( "#down-"+post_pk ).html( 'downvote' )
           }
      });
    } else if ( $( me ).hasClass('upvoted-arrow') ) {
      $.ajax({
        type:"GET",
        url: url,
        success: function(data){
          $( me ).addClass('up-arrow').removeClass('upvoted-arrow').removeClass('active-vote');
          $( "#commentscore-pk-"+post_pk ).html( data )
          $( "#up-"+post_pk ).html( 'upvote' )
        }
      });
    }


  });


});

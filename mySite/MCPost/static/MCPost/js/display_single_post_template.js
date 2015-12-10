base_namespace.display_single_post_template = base_namespace.display_single_post_template || {};

$(document).ready(function() {

  // make sure this javascript file is only loaded once
  if (!isFirstLoad(base_namespace.display_single_post_template)) {
    return;
  }

  // this implements history button functionality
  $( ".comment-all").hide()   // only show last post/edit and hide all previous
  $( ".comment-last").show()
  $( "a[id*='action-']" ).click(function(e) {   // dropdown to select which revision to view
    var action_pk_counter = $(this).attr("id")
    var arr = action_pk_counter.split('-')
    var pk = arr[1]
    var counter = arr[2]
    $( ".li-dropdown-" + pk).removeClass("active");
    $( ".li-dropdown-"+pk+"-"+counter).addClass("active");
    var time_text = $( ".li-dropdown-"+pk+"-"+counter+ " > a" ).html();
    $( "#comment-time-"+pk).html(time_text)
    $( ".comment-target-all-" + pk).hide()
    $( "#comment-text-" + pk + "-" + counter).show()
  });

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


  // this implements delete post functionality
  $('.delete-post-are-you-sure').hide()
  $('.delete-post-confirmation').hide()
  $('.delete-post-button').click(function(e) {
    $(this).hide()
    $(this).next('.delete-post-are-you-sure').show()
  });
  $('.delete-post-no').click(function(e) {
    $(this).parent().prev('.delete-post-button').show()
    $(this).parent('.delete-post-are-you-sure').hide()
  });
  $(".delete-post-yes").click(function() {
    f = $(this).next('form');
    var url = f.attr( 'action' );
    $.ajax({
      type: "POST",
      url: url,
      data: f.serialize(),
      success: function(data) { // update post to be deleted
        f.parent('.delete-post-are-you-sure').hide()
        f.parent('.delete-post-are-you-sure').next('.delete-post-confirmation').show()
      }
    });
  });

  // this makes toggles stay up even when clicked
  $('.no-closing-dropdown a').on('click', function (event) {
    $(this).parent().toggleClass('open');
  });
  $('body').on('click', function (e) {
      if (!$('.no-closing-dropdown').is(e.target)
          && $('.no-closing-dropdown').has(e.target).length === 0
          && $('.open').has(e.target).length === 0
      ) {
          $('.no-closing-dropdown').removeClass('open');
      }
  });

});

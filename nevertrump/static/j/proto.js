$(document).ready(function() {
// Handler for .ready() called.
	
	$('.button').on('click', function() {
		$('.button').removeClass('active');
		$(this).addClass('active');
	});

});
	   	
	
	
$(window).load(function() {
   $('.content').each(function(i) {
      $(this).fadeIn(400);
   });
});

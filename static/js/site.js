
	$(document).ready( function() {
		function beforeEditSubmit() {
			$(".edit-form").find("input, textarea").attr('disabled', true);
			$("#progress-gif").fadeIn('slow');
		};
		function afterEditSubmit() {
			$("#progress-gif").fadeOut('slow');
			setTimeout( function() {
				$(".edit-form").find("input, textarea").attr('disabled', false);
			}, 1000);
		};
		
		$(".edit-form").ajaxForm({

			beforeSubmit: beforeEditSubmit,
			success: afterEditSubmit
			}); 
});
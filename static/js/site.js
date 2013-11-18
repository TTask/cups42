
	$(document).ready( function() {


		function showResult(responseText){
			var $resultField = $("#result");
			$resultField.empty();
			$resultField.append(responseText['request_result']);
			if (responseText['request_result'] == 'Error occurred') {
				for(var key in responseText){
					$('input[name=' + key + ']').addClass('error-input').val(responseText[key]).focus();
				};
			};
		};


		function beforeEditSubmit() {
			$(".edit-form").find("input, textarea").attr('disabled', true);
			$(".edit-form").find(".error-input").removeClass('error-input');
			$("#progress-gif").fadeIn('slow');

		
		};


		function afterEditSubmit(responseText, statusText, xhr, $form) {
			$("#progress-gif").fadeOut('slow');
			setTimeout( function() {
				$(".edit-form").find("input, textarea").attr('disabled', false);
			}, 1000);
			showResult(responseText)
		};

		
		function result(responseText, statusText, xhr, $form){
			alert(responseText['birth_date']);
		};
		$(".edit-form").ajaxForm({

			beforeSubmit: beforeEditSubmit,
			success: afterEditSubmit,
			fail: afterEditSubmit,
			url: '/edit_ajax',
			dataType: 'json'
			}); 
});

	$(document).ready( function(){

		function clearFileInput(){
    			var oldInput = document.getElementById("id_photo");
    			var newInput = document.createElement("input");
    			newInput.type = "file";
    			newInput.id = oldInput.id;
    			newInput.name = oldInput.name;
    			newInput.className = oldInput.className;
    			newInput.style.cssText = oldInput.style.cssText;
    			oldInput.parentNode.replaceChild(newInput, oldInput);
			};

		function showResult(responseText){
			var $resultField = $("#result");
			$resultField.empty();
			$resultField.append(responseText['request_result']);
			if (responseText['request_result'] == 'Error occurred') {
				for(var key in responseText){
					$('input[name=' + key + ']').addClass('error-input').attr('placeholder', (responseText[key])).val("").focus();
				};
			};
		};

		function beforeEditSubmit(){
			$(".edit-form").find("input, textarea").attr('disabled', true);
			$(".edit-form").find(".error-input").removeClass('error-input');
			$("#progress-gif").fadeIn('slow');
		};

		function afterEditSubmit(responseText, statusText, xhr, $form) {
			$("#progress-gif").fadeOut('slow');
			setTimeout( function(){
				$(".edit-form").find("input, textarea").attr('disabled', false);
			}, 1000);
			showResult(responseText);
			clearFileInput();
		};

		$(".edit-form").ajaxForm({
			beforeSubmit: beforeEditSubmit,
			success: afterEditSubmit,
			fail: afterEditSubmit,
			url: '/edit_ajax',
			dataType: 'json'
			});

		function afterPriorityEditSubmit(responseText, statusText, xhr, $form){
			$($form).find('input').attr('disabled', false);
			$("#progress-gif").fadeOut('slow');
			showResult(responseText);
		};

		function beforePriorityEditSubmit(){
			var $form = $('#change-request-priority');
			$form.find(".error-input").removeClass('error-input');
			$form.find('input').attr('disabled', true);
			$("#progress-gif").fadeIn('slow');
		};

		$("#change-request-priority").ajaxForm({
			beforeSubmit: beforePriorityEditSubmit,
			success: afterPriorityEditSubmit,
			fail: afterPriorityEditSubmit,
			url: '/edit_request_priority',
			dataType: 'json'
		});

		$(".request-path").on('click', function(event){
			event.preventDefault();
			$('#id_request_path').val($(this).text());
		});
});

$(document).ready(function() {
	init();
	$('.weight-input').change(function() {
		if (!calculateTotal(true)) {
			// if there is an error with the total then empty the weight field that caused the error
			$(this).val('');
			$(this).focus();
			// update the total label but without removing the error, because the error just generated
			calculateTotal(false);
		}
	});
	function init() {
		// add the appropriate class name to weight inputs because the fields when saved with the form
		// are generated through it, so we need to add this class
		$('.field-input-wrapper input').each(function() {
			$(this).attr('class', 'weight-input');
		});
		calculateTotal(true);
	}
	function calculateTotal(removeError) {
		var total = 0;
		// calculate the total weight from the input fields
		$('.weight-input').each(function(event) {
			value = $(this).val();
			var valueToAdd = 0;
			if (value != '') {
				valueToAdd = parseInt(value);
			}
			total += valueToAdd;
		});
		// the total can be null if a non-numerical value entered
		if (total) {
			if (total >= 0 && total <= 100) {
				// update the total weight label
				$('#weight-total').text(total.toString());
				// because we calculate the total in every occasion, we want to remove the previous
				// generated error only when there is no error yet
				if (removeError) {
					$('.errorlist').children().each(function() {
						$(this).remove();
					});
				}
				return true;
			} else {
				// show the error
				if ($('.errorlist').children().length < 1) {
					$('.errorlist').append('<li>The weight total must be less than or equal to 100</li>');
				}
				return false;
			}
		}
	}
});
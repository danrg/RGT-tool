$(document).ready(function () {
	init();
	$('.weight-input').change(function () {
		calculateTotal();
	});
	function init() {
		// add the appropriate class name to weight inputs because the fields when saved with the form
		// are generated through it, so we need to add this class
		$('.field-input-wrapper input').each(function() {
			$(this).attr('class', 'weight-input');
		});
		// focus on the first weight on load
		$('#id_3-weight1').focus();
		calculateTotal();
	}
	function calculateTotal() {
		var total = 0;
		// calculate the total weight from the input fields
		$('.weight-input').each(function(event) {
			value = $(this).val();
			var valueToAdd = 0;
			if (value != '') {
				valueToAdd = parseInt(value);
			}
			if (valueToAdd) { total += valueToAdd; }
		});
		// update the total weight label
		$('#weight-total').text(total.toString());
	}
});
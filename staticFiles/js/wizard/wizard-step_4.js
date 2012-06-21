$(document).ready(function() {
	init();
	$('.weight-input').change(function() {
		calculateTotal();
	});
	function init() {
		$('.field-input-wrapper input').each(function() {
			$(this).attr('class', 'weight-input');
		});
		calculateTotal();
	}
	function calculateTotal() {
		var total = 0;
		$('.weight-input').each(function(event) {
			value = $(this).val();
			var valueToAdd = 0;
			if (value != '') {
				valueToAdd = parseInt(value);
			}
			total += valueToAdd;
		});
		if (total >= 0 && total <= 100) {
			$('#weight-total').text(total.toString());
		} else {
			alert('The weight total must be greater than 0 and less than 100.');
		}
	}
});
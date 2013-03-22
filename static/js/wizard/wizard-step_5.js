$(document).ready(function () {
	init();
	$('#alternatives-list').change(function (event) {
		setAlternativeName($('#alternatives-list').val());
		updateRadioButtonsWithRatings();
	});
	$('.rating').change(function() {
		// get the rating value of the selected radio button
		var ratingValue = $(this).val();
		// get the id of the selected radio button
		var ratingIdAttr = $(this).attr('id');
		// get the index of the selected alternative in the list
		var alternativeIndex = $('#alternatives-list option:selected').index();
		// get the concern index after splitting the id of the selected radio button and keeping the
		// first value, the id has the form (concernIndex-value)
		var concernIndex = ratingIdAttr.split('-')[0];
		// change the appropriate hidden field rating with the value of the radio button
		$('#id_4-rating-concern' + concernIndex + '-alternative' + (alternativeIndex + 1)).val(ratingValue);
		checkRatingsCompleted();
	});
	function init() {
		setAlternativeName($('#alternatives-list').val());
		updateRadioButtonsWithRatings();
		checkRatingsCompleted();
	}
	function setAlternativeName(text) {
		$('#alternative-name').text(text);
	}
	function updateRadioButtonsWithRatings() {
		// get the number of concerns
		var numberOfConcerns = $('#num-concerns').val();
		// get the index of the selected alternative in the list
		var alternativeIndex = $('#alternatives-list option:selected').index();
		// the array to hold the ratings values
		var ratingValues = new Array();
		// fill the array with the values from the hidden fields according to the indexes
		for (var i = 0; i < numberOfConcerns; i++) {
			ratingValues[i] = $('#id_4-rating-concern' + (i + 1) + '-alternative' + (alternativeIndex + 1)).val();
		}
		// un_check all radio buttons 
		$('.rating').each(function() {
			$(this).removeAttr('checked');
		});
		// check those radio buttons according to the values of the hidden fields
		for (i=0;i<numberOfConcerns;i++) {
			$('#' + (i + 1) + '-'+ratingValues[i]).attr('checked', 'checked');
		}
	}
	function checkRatingsCompleted() {
		$('.rca-data').each(function(index) {
			var incomplete = false;
			// for each hidden field, if the value is 0 or it different than number then the
			// alternative is incomplete
			$(this).children().each(function() {
				var v = $(this).val();
				if ((v == '0') || !(parseFloat(v))) { incomplete = true; }
			});
			// indicate the incomplete alternative
			if (incomplete) {
				$('#alternatives-list option[id="alternative-'+(index+1)+'"]').attr('class', 'incomplete');
			} else {
				$('#alternatives-list option[id="alternative-'+(index+1)+'"]').removeAttr('class');
			}
		});
	}
});
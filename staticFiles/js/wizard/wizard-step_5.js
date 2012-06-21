$(document).ready(function() {
	init();
	$('#alternatives-list').change(function(event) {
		setAlternativeName($('#alternatives-list').val());
		var numberOfConcerns = $('#num-concerns').val();
		var alternativeIndex = event.target.options.selectedIndex;
		var ratingValues = new Array();
		for (i=0;i<numberOfConcerns;i++) {
			ratingValues[i] = $('#id_4-rating-concern'+(i+1)+'-alternative'+(alternativeIndex+1)).val();
		}
		$('.rating').each(function() {
			$(this).removeAttr('checked');
		});
		for (i=0;i<numberOfConcerns;i++) {
			$('#'+(i+1)+'-'+ratingValues[i]).attr('checked', 'checked');
		}
	});
	$('.rating').change(function() {
		var ratingValue = $(this).val();
		var ratingIdAttr = $(this).attr('id');
		var splitted = ratingIdAttr.split('-');
		var alternativeIndex = $('#alternatives-list option:selected').index();
		var concernIndex = splitted[0];
		$('#id_4-rating-concern'+concernIndex+'-alternative'+(alternativeIndex+1)).val(ratingValue);
		checkRatingsCompleted();
	});
	function init() {
		setAlternativeName($('#alternatives-list').val());
		checkRatingsCompleted();
	}
	function setAlternativeName(text) {
		$('#alternative-name').text(text);
	}
	function checkRatingsCompleted() {
		$('.rca-data').each(function(index) {
			var incomplete = false;
			$(this).children().each(function() {
				incomplete = ($(this).val() === '0') ? true : false;
			});
			if (incomplete) {
				$('#alternatives-list option[id="alternative'+(index+1)+'"]').attr('class', 'incomplete');
			} else {
				$('#alternatives-list option[id="alternative'+(index+1)+'"]').removeAttr('class');
			}
		});
	}
});
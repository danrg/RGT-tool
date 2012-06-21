$(document).ready(function() {
	setAlternativeName($('#alternatives-list').val());
	$('#alternatives-list').change(function(event) {
		setAlternativeName($('#alternatives-list').val());
		var numberOfConcerns = $('.rating-input').length;
		var alternativeIndex = event.target.options.selectedIndex;
		var ratingValues = new Array();
		for (i=0;i<numberOfConcerns;i++) {
			ratingValues[i] = $('#id_4-rating-concern'+(i+1)+'-alternative'+(alternativeIndex+1)).val();
		}
		$('.rating-input').each(function(index) {
			$(this).val(ratingValues[index]);
		});
	});
	$('#save-button').click(function(event) {
		var ratingValues = new Array();
		$('.rating-input').each(function(index) {
			ratingValues[index] = $(this).val();
		});
		var alternativeIndex = $('#alternatives-list option:selected').index();
		var numberOfConcerns = $('.rating-input').length;
		for (i=0;i<numberOfConcerns;i++) {
			$('#id_4-rating-concern'+(i+1)+'-alternative'+(alternativeIndex+1)).val(ratingValues[i]);
		}
	});
	function setAlternativeName(text) {
		$('#alternative-name').text(text);
	}
	$('.rating-input').keyup(function(event) {
		switch (event.keyCode) {
		}
		console.log(event.keyCode);
	});
});
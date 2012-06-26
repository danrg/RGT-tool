$(document).ready(function() {
	$('.drag').draggable({
		start: function(event, ui) {
			console.log('start');
			var i = event.target;
			$(i).css('z-index', '1');
		},
		stop: function(event, ui) {
			console.log('stop');
		}
	});
	$('.drop').droppable({
		drop: function(event, ui) {
			// make the element draggable again so it can be moved to another list
			var i = ui.draggable;
			$(this).append(i.clone().attr('style', 'position: relative;').attr('class', 'drag ui-draggable').draggable());
			// remove the element from the previous list
			$(i).remove();
		}
	});
	
	$('#add-conc-but').click(function() {
		// get references of the left and right part of the concerns the user inserted
		var lcField = $('#left-conc');
		var rcField = $('#right-conc');
		// get the number of cloned inputs
		var numOfCloned = $('.cloned').length;
		console.log(numOfCloned);
		// this is the new number
		var newNum = numOfCloned + 1;
		// get the values of the right and left concern that the user inserted
		var leftConcValue = lcField.val();
		var rightConcValue = rcField.val();
		// continue only if values are inserted
		if (leftConcValue != "" && rightConcValue != "") {
			// construct the ids and the names of the new created fields that will become part of the form fields
			var leftId = "id_2-concern"+newNum+"-left";
			var rightId = "id_2-concern"+newNum+"-right";
			var leftName = "2-concern"+newNum+"-left";
			var rightName = "2-concern"+newNum+"-right";
			// append the new concern with the left and right pole on the concern list
			if (numOfCloned == 0) {
				$('#conc-list-data').empty();
			}
			$('#conc-list-data').append('<div id="input'+newNum+'" class="cloned"><input type="text" name="'+leftName+'" value="'+leftConcValue+'" id="'+leftId+'" /><input type="text" name="'+rightName+'" value="'+rightConcValue+'" id="'+rightId+'" /></div>');
			// put the new number of concerns
			$('#num-concerns').val(newNum);
			// clear the values
			lcField.val('');
			rcField.val('');
		}
	});
});
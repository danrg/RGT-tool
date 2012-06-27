$(document).ready(function() {
	$('.drag').draggable({
		revert: 'invalid'
	});
	$('.drop').droppable({
		drop: function(event, ui) {
			// get the draggable element of the event
			var i = ui.draggable;
			// append the element to the new list and make it draggable again so it can be moved to another list
			$(this).append(i.clone().attr('style', 'position: relative;').attr('class', 'drag ui-draggable').draggable({revert: 'invalid'}));
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
			// if this is the first pair being added remove the 'no concerns yet' info message
			if (numOfCloned == 0) {
				$('#conc-list-data').empty();
			}
			// construct the left concern, right concern and separator fields
			var leftConc = "<div class='field-wrapper'><div class='field-input-wrapper'><input id='"+leftId+"' type='text' name='"+leftName+"' value='"+leftConcValue+"' size='50' /></div></div>";
			var rightConc = "<div class='field-wrapper'><div class='field-input-wrapper'><input id='"+rightId+"' type='text' name='"+rightName+"' value='"+rightConcValue+"'  size='50' /></div></div>"
			var sep = "<div class='sep'><span>--</span></div>";
			// append the new concern with the left and right pole on the concern list
			$('#conc-list-data').append('<div id="input'+newNum+'" class="cloned">'+leftConc+sep+rightConc+'</div>');
			// put the new number of concerns
			$('#num-concerns').val(newNum);
			// clear the values
			lcField.val('');
			rcField.val('');
		}
	});
});
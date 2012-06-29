$(document).ready(function() {
	$('.drag').draggable({
		revert: 'invalid',
		start: function(event, ui) {
			$(this).css('z-index', '10000');
		},
		stop: function(event, ui) {
			$(this).css('z-index', '');
		}
	});
	$('.drop').droppable({
		drop: function(event, ui) {
			// get the draggable element of the event
			var i = ui.draggable;
			// append the element to the new list and make it draggable again so it can be moved to another list
			$(this).append(i.clone().attr('style', 'position: relative;').attr('class', 'drag ui-draggable').draggable({revert: 'invalid', start: function(event, ui) {
				$(this).css('z-index', '10000');
			}}));
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
			// reset the alternatives
			reset($('#sim-list-data'));
			reset($('#diff-list-data'));
		} else {
			showMessageInDialogBox('Please first type the left and right pole of the concern and then press the "Add" button.');
		}
	});
	$('#form').submit(function(event) {
		// get references of the left and right part of the concerns the user inserted
		var lcField = $('#left-conc');
		var rcField = $('#right-conc');
		// get the values of the right and left concern that the user inserted
		var leftConcValue = lcField.val();
		var rightConcValue = rcField.val();
		// if one of the fields for the concerns have a value, show a dialog to the user to decide
		// if he wants to keep the values or discard
		if (leftConcValue != "" || rightConcValue != "") {
			// get the dialog div and put the message
			dialogDiv= getDialogDiv();
			dialogDiv.html('<p>You have typed a concern but you have not added yet by pressing the "Add" button. If you got to next step this data will be lost. Do you still want to go to next step?</p>');
			// show the dialog
			dialogDiv.dialog({
				title: 'Information',
				resizable: false,
				height: 150,
				width: 450,
				modal: true,
				buttons: {
					"Next Step": function() {
						$(this).dialog("close");
						// clear the values if user selects 'Next Step' so the form
						// can be submitted successfully
						lcField.val('');
						rcField.val('');
						$('#form').submit();
					},
					Cancel: function() {
						$(this).dialog("close");
					}
				}
			})
			return false;
		}
	});
	function reset(list) {
		list.children().each(function() {
			// first remove the alternative and then append it to the alternative list
			$(this).remove();
			$('#alt-list-data').append($(this).attr('style', 'position: relative;').attr('class', 'drag ui-draggable').draggable({revert: 'invalid', start: function(event, ui) {
				$(this).css('z-index', '10000');
			}}));
		});
	}
});
$(document).ready(function () {
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
			var leftId = "id_2-concern" + newNum + "-left";
			var rightId = "id_2-concern" + newNum + "-right";
			var leftName = "2-concern" + newNum + "-left";
			var rightName = "2-concern" + newNum + "-right";
			// if this is the first pair being added remove the 'no concerns yet' info message
			if (numOfCloned == 0) {
				$('#conc-list-data').empty();
			}
			// construct the left concern, right concern and separator fields
			var leftConc = "<div class='field-wrapper'><div class='field-input-wrapper'><input id='" + leftId + "' type='text' name='" + leftName + "' value='" + leftConcValue + "' size='50' /></div></div>";
			var rightConc = "<div class='field-wrapper'><div class='field-input-wrapper'><input id='" + rightId + "' type='text' name='" + rightName + "' value='" + rightConcValue + "'  size='50' /></div></div>";
			var sep = "<div class='sep'><span>--</span></div>";
            var deleteButton = "<div class=\"del-conc-but-wrapper\"><input type=\"button\" class=\"del-conc-but\" value=\"Delete\" /></div>";

			// append the new concern with the left and right pole on the concern list
			$('#conc-list-data').append('<div id="input' + newNum + '" class="cloned">' + leftConc + sep + rightConc + deleteButton + '</div>');
			// put the new number of concerns
			$('#num-concerns').val(newNum);
			// clear the values
			lcField.val('');
			rcField.val('');
			// construct the acrd, acrd stands for alternative-concern-relation-data
			constructACRD($('#sim-list-data'), newNum, 1);
			constructACRD($('#diff-list-data'), newNum, 5);
			// reset the alternatives
			reset($('#sim-list-data'));
			reset($('#diff-list-data'));
		} else {
			showMessageInDialogBox('Please first type the left and right pole of the concern and then press the "Add" button.');
		}
	});

    $(document).on("click", ".del-conc-but", function () {
        // get the number of cloned inputs
        var numOfCloned = $('.cloned').length;
        // this is the new number
        var newNum = numOfCloned - 1;
        if (numOfCloned >= 2) {
            var wrapper = $(this).closest($('.cloned'));
            var removedIndex = parseInt(wrapper.attr('id').substring(5));
            wrapper.remove();

            // Rearrange indices
            for(var i = removedIndex + 1; i <= numOfCloned; i++) {
                $('#input' + i).attr('id', 'input' + (i - 1));
                $('#id_2-concern' + i + '-left').attr({
                    'id': 'id_2-concern' + (i - 1) + '-left',
                    'name': '2-concern' + (i - 1) + '-left'
                });
                $('#id_2-concern' + i + '-right').attr({
                    'id': 'id_2-concern' + (i - 1) + '-right',
                    'name': '2-concern' + (i - 1) + '-right'
                });
            }

            $('.cloned').length = newNum;
            $('#num-concerns').attr('value', newNum);
        } else {
            showMessageInDialogBox('At least 2 concern pairs should exist to perform delete.');
        }
    });
	$('#form').submit(function(event) {
		// get references of the left and right part of the concerns the user inserted
		var lcField = $('#left-conc');
		var rcField = $('#right-conc');
		// get the values of the right and left concern that the user inserted
		var leftConcValue = lcField.val();
		var rightConcValue = rcField.val();
		// if one of the fields for the concerns have a value, show a dialog to the user to dec ide
		// if he wants to keep the values or discard
		if (leftConcValue != "" || rightConcValue != "") {
			// get the dialog div and put the message
			dialogDiv= getDialogDiv();
			dialogDiv.html('<p>You have typed a concern which you have not added yet by pressing the "Add" button. If you go to the next step this data will be lost. Do you still want to go to the next step?</p>');
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
	function constructACRD(list, concIndex, rating) {
		list.children().each(function(index) {
			// get the alternative index from the id of the placed alternative in the list
			var altIndex = $(this).attr('id').split('-')[1];
			// get the number of acrd already exist
			var acrd = $('.acrd').length;
			// construct id, name and value
			var id = "id_2-acrd"+(acrd+1);
			var name = "2-acrd"+(acrd+1);
			var value = altIndex+"-"+concIndex+"-"+rating;
			// construct the hidden elem
			var elem = "<input id='"+id+"' type='hidden' class='acrd' value='"+value+"' name='"+name+"' />";
			// append the elem in the acrd list
			$('#alt-conc-rel-data').append(elem);
			// increase the number of acrd
			$('#num-acrd').val(acrd+1);
		});
	}
});

$(document).ready(function() {
	$('.drag').draggable();
	$('.drop').droppable({
		drop: function(event, ui) {
			var i = ui.draggable;
			$(this).append(i.clone().attr('style', 'position: relative;').draggable());
			$(i).remove();
		}
	});
	
	$('#add-conc-but').click(function() {
		// get references of the left and right part of the concerns thea the user inserted
		var lcField = $('#left-conc');
		var rcField = $('#right-conc');
		// get the number of clonded inputs
		var numOfCloned = $('.cloned').length;
		// this is the new number
		var newNum = numOfCloned + 1;
		// get the values of the right and left concern that the user inserted
		var leftConcValue = lcField.val();
		var rightConcValue = rcField.val();
		// construct the ids and the names of the new created fields that will become part of the form fields
		var leftId = "id_2-concern"+newNum+"-left";
		var rightId = "id_2-concern"+newNum+"-right";
		var leftName = "2-concern"+newNum+"-left";
		var rightName = "2-concern"+newNum+"-right";
		// append the new concern with the left and right pole on the concern list
		$('#conc-list').append('<div id="input'+newNum+'" class="cloned"><input type="text" name="'+leftName+'" id="'+leftId+'" value="'+leftConcValue+'" /><input type="text" name="'+rightName+'" id="'+rightId+'" value="'+rightConcValue+'" /></div>');
		// put the new number of concerns
		$('#numConcernPairs').val(newNum);
		// clear the values
		lcField.val('');
		rcField.val('');
	});
});
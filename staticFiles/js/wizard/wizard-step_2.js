$(document).ready(function() {
	$('#btn-add').click(function() {
		// how many cloned input fields there are currently
	    var num = $('.cloned').length;
	    // the numeric ID of the new input field being added
	    var newNum = new Number(num + 1);
	    // update count of alternatives
	    $('#num-alternatives').val(newNum);
	    // create the new element
	    var newElem	= '<div id="input'+newNum+'" class="cloned"><input type="text" name="1-alternative'+newNum+'" id="id_1-alternative'+newNum+'" /></div>'
	    // insert the new element after the last input field
	    $('#input' + num).after(newElem);
	});
});
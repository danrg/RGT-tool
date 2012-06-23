$(document).ready(function() {
	$('#btn-add').click(function() {
		// how many cloned input fields there are currently
	    var num = $('.cloned').length;
	    // the numeric ID of the new input field being added
	    var newNum = new Number(num + 1);
	    // update count of alternatives
	    $('#num-alternatives').val(newNum);
	    // create the new element
	    var divId = 'input'+newNum;
	    var inputName = '1-alternative'+newNum;
	    var inputId = 'id_1-alternative'+newNum;
	    var newElem	= '<div id="'+divId+'" class="cloned"><input type="text" name="'+inputName+'" id="'+inputId+'" /></div>'
	    // insert the new element after the last input field
	    $('#input' + num).after(newElem);
	    // focus on the new element
	    $('#'+inputId).focus();
	});
});
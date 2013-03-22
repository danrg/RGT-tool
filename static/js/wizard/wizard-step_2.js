$(document).ready(function () {
	init();
	$('#btn-add').click(function () {
		// how many cloned input fields there are currently
        var num = $('.cloned').length;
        // the numeric ID of the new input field being added
        var newNum = new Number(num + 1);
        // update count of alternatives
        $('#num-alternatives').val(newNum);
        // create the new element
        var divId = 'input'+newNum;
        var inputName = '1-alternative-' + newNum;
        var inputId = 'id_1-alternative-' + newNum;
        //create the new button
        var buttonId = 'btn-del-' + newNum;
        var removefun = 'removeAlt('+newNum+')';
        var newElem	= '<div id="' + divId + '" class="cloned"><input type="text" name="' + inputName + '" id="' + inputId + '" tabindex="' + newNum + '" size="30" /> <input type="button" id="' + buttonId + '" value="X" onclick="' + removefun + '" /></div>';
        // insert the new element after the last input field
        $('#input' + num).after(newElem);
        // focus on the new element
        $('#' + inputId).focus();
        // update the tab indexes of the rest elements
        $('#btn-add').attr('tabindex', newNum + 1);
        $('#btn-submit').attr('tabindex', newNum + 2);
        $('#btn-prev-step').attr('tabindex', newNum + 3);
	});
	function init() {
		// focus on the first alternative input
		$('#id_1-alternative-1').focus();
	}
});
function removeAlt(buttonNumber) {
    // how many cloned input fields there are currently
    var num = $('.cloned').length;
    // the numeric ID after the textbox is deleted
    var newNum = new Number(num - 1);
    var delElement = $(this).find('#input' + buttonNumber);
    // delete element
    if (num > 2) {
        $('#input' + buttonNumber).remove();
        // update count of alternatives
        $('#num-alternatives').val(newNum);
        var i = new Number(buttonNumber + 1);
        var j = 0;
        for (i; i <= num; i++) {
            j = i - 1;
            $('#input' + i).attr('id', 'input' + j);
            $('#id_1-alternative-' + i).attr('name', '1-alternative-' + j);
            $('#id_1-alternative-' + i).attr('tabindex', j);
            $('#id_1-alternative-' + i).attr('id', 'id_1-alternative-' + j);
            $('#btn-del-' + i).attr('onclick', 'removeAlt(' + j + ')');
            $('#btn-del-' + i).attr('id', 'btn-del-' + j);
        }
        //update tabindexes
        $('#btn-add').attr('tabindex', newNum);
        $('#btn-submit').attr('tabindex', newNum + 1);
        $('#btn-prev-step').attr('tabindex', newNum + 2);
    } else {
        showMessageInDialogBox('Atleast more than 2 alternatives should exist to perform delete.');
    }
}

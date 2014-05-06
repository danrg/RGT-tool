$(document).ready(function () {
    $('#id_1-alternative-1').focus();
    $('form').submit(function() {
        removeEmptyAlts();
    });
});

function removeAlt(altIndex) {
    if ($('.cloned').length > 2) {
       doRemoveAlt(altIndex);
    } else {
        showMessageInDialogBox('More than two alternatives should exist to perform delete.');
    }
}

function doRemoveAlt(altIndex) {
    // how many cloned input fields there are currently
    var num = $('.cloned').length;
    // the numeric ID after the textbox is deleted
    var newNum = new Number(num - 1);
    var delElement = $(this).find('#input' + altIndex);
    // delete element
    $('#input' + altIndex).remove();
    // update count of alternatives
    $('#num-alternatives').val(newNum);
    var i = new Number(altIndex + 1);
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
}

function removeEmptyAlts() {
    $('.cloned input:text[value=""]').each(function() {
        var index = parseInt($(this).attr('id').substring("id_1-alternative-".length));
        doRemoveAlt(index);
    });
}

$(document).on('focus', '.cloned input[type=text]', function() {
    var numEmpty = $('.cloned input:text[value=""]').length;
    var numEmptyRequired = 2;
    if ($(this).val()) {
        numEmptyRequired--;
    }
    if(numEmpty < numEmptyRequired) {
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
        // update the tab indexes of the rest elements
        $('#btn-add').attr('tabindex', newNum + 1);
        $('#btn-submit').attr('tabindex', newNum + 2);
        $('#btn-prev-step').attr('tabindex', newNum + 3);
    }
});
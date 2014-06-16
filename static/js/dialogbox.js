function showMessageInDialogBox(text) {
	showMessageInDialogBox(text, null);
}

function showMessageInDialogBox(text, closeFunction) {
	buttons = {
        'Close': function () {
            $(this).dialog("close");
            if (closeFunction != null) {
                closeFunction();
            }
        }
    }
    showMessageInBox(text, buttons);
}

function showMessageInConfirmBox(text, confirmFunction) {
    buttons = {
        'Ok': function () {
            $(this).dialog("close");
            if (confirmFunction != null) {
                confirmFunction();
            }
        },
        'Cancel': function() {
            $(this).dialog("close");
        }
    };
    showMessageInBox(text, buttons);
}

function showMessageInBox(text, buttons, height, width) {
    if(height === undefined) {
        height = 160;
    }
    if(width === undefined) {
        width = 400;
    }

    $('#modalDialogBox').html('<p>' + text + '</p>');
	$('#modalDialogBox').dialog({
		title: 'Information',
		resizable: false,
		height: height,
		width: width,
		modal: true,
		buttons: buttons
	});
}

function getDialogDiv() {
	return $('#modalDialogBox');
}

function showMessageInDialogBox(text) {
	showMessageInDialogBox(text, null);
}

function showMessageInDialogBox(text, closeFunction) {
	$('#modalDialogBox').html('<p>' + text + '</p>');
	$('#modalDialogBox').dialog({
		title: 'Information',
		resizable: false,
		height: 160,
		width: 400,
		modal: true,
		buttons: {'Close':function () {
				$(this).dialog("close");
				if (closeFunction != null)
				{
					closeFunction();
				}
			}
		}
	});
}

function showMessageInConfirmBox(text, confirmFunction) {
    $('#modalDialogBox').html('<p>' + text + '</p>');
	$('#modalDialogBox').dialog({
		title: 'Information',
		resizable: false,
		height: 160,
		width: 400,
		modal: true,
		buttons: {
                'Ok': function () {
                    $(this).dialog("close");
                    if (confirmFunction != null)
                    {
                        confirmFunction();
                    }
			    },
                'Cancel': function() {
                    $(this).dialog("close");
                }
		}
	});
}

function showMessageInBox(text, buttons) {
    $('#modalDialogBox').html('<p>' + text + '</p>');
	$('#modalDialogBox').dialog({
		title: 'Information',
		resizable: false,
		height: 160,
		width: 400,
		modal: true,
		buttons: buttons
	});
}

function getDialogDiv()
{
	return $('#modalDialogBox');
}

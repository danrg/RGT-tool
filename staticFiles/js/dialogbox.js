function showMessageInDialogBox(text) {
	$('#modalDialogBox').html('<p>' + text + '</p>');
    $('#modalDialogBox').dialog({
    	title: 'Information',
		resizable: false,
		height: 160,
		width: 400,
		modal: true,
		buttons: {'Close':function(){
				$( this ).dialog( "close" );
			}
    	}
    });
}

function getDialogDiv()
{
	return  $('#modalDialogBox');
}

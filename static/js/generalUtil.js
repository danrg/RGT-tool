/**
 * This function will retrieve the download image page and place it inside a modal dialog box.
 * @param hiddenData object with the arguments that should be passed to the server, format: { argumentName: value, argumentName: value, ......}
 */
function downloadImageOf(formUrl, hiddenData)
{
	if (formUrl != null)
	{
		//the double function is used here so the tagData obj will be able to be used inside the function that will handle the post response
		var callBack = function (formUrl, hiddenData)
		{
			return function (data)
			{
				if ($(data).find('error').length <= 0)
				{
					var modalDiv = getDialogDiv();
					modalDiv.html($(data).find('htmlData').text());
					var form = modalDiv.find('form');
					var temp = null;
					if (hiddenData != null)
					{
						for (attrib in hiddenData)
						{
							temp = $('<input>').attr("type", "hidden").attr("name", attrib).val(hiddenData[attrib]);
							form.append($(temp));
						}
					}
					form.attr('action', formUrl);
					modalDiv.dialog({
						title: 'Download',
						resizable: false,
						width:400,
						modal: true,
						buttons: {'Download':function () {
							sendDownloadSvgForm();
							}
                        }
                    });
				}
				else
				{
					showMessageInDialogBox($(data).html('error').text());
				}
			}
		}
		//get the download form
		$.post('/grids/download/', '', callBack(formUrl, hiddenData));
	}
	else
	{
		showMessageInDialogBox('Error in javascript, no form url was set');
		console.log('Error, no form url was set')
	}
}
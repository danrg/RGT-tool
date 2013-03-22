var urlStaticFiles = '/static/';
var loadingDiv = $('#wrap');
var hasTableBeenSaved = true;
var masterFormString = '';

function showMySession()
{
	showLoadingSpinner(loadingDiv, null);
	try
	{
		var sessionUSID = mySessionsGetSessionUSID();
		if(sessionUSID != 'noSessions' && sessionUSID != '' && sessionUSID != null)
		{
			var str = 'sessionUSID=' + sessionUSID;
			$.post('/sessions/show/', str, function(data){
				try
				{
					//if(data.search('<error>.*?</error>') <= -1)
					if ($(data).find('error').length <= 0)
					{
						$('#concentDiv').html($(data).find('htmlData').text());
						prepareForNewGrid($('#contentDiv'));
						//set tipsy
						initiateGridTableToolTip($('#concentDiv'));
						hideLoadingSpinner(loadingDiv);
						hasTableBeenSaved = true;
						masterFormString = $('#form').serialize();
						//initialize anything that should be initialize after the content page has loaded
						initializeMySessionsContent(); // from mySessionsContent.js
					}
					else
					{
						//error handling
						hideLoadingSpinner(loadingDiv);
						showMessageInDialogBox($(data).find('error').text());
					}
				}
				catch(err)
				{
					hideLoadingSpinner(loadingDiv);
					console.log(err);
				}
			});
		}
		else
		{
			hideLoadingSpinner(loadingDiv);
		}
	}
	catch(err)
	{
		hideLoadingSpinner(loadingDiv);
		console.log(err);
	}
}

function mySessionsGetSessionUSID()
{
	return $("#mySessionsSelect option:selected").val();
}

function getContentDivId()
{
	return 'concentDiv';
}

function isTableSaved()
{
	if(masterFormString != $("#form").serialize())
	{
		if(hasTableBeenSaved)
		{
			changeTableSaveStatusIcon($('#concentDiv'), false);
			setGridTableSaveStatusToolTip($('#concentDiv'), 'Current showing table has been modified since retrieving it from the server.');
			hasTableBeenSaved= false;
		}
	}
	else
	{
		if(!hasTableBeenSaved)
		{
			changeTableSaveStatusIcon($('#concentDiv'), true);
			setGridTableSaveStatusToolTip($('#concentDiv'), 'Current showing table has not been modified since retrieving it from the server.');
			hasTableBeenSaved= true;
		}
	}
}

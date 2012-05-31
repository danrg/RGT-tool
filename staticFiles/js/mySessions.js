var urlStaticFiles= '/static/'
var loadingDiv= $('#wrap');
var hasTableBeenSaved = true;
var masterFormString = '';

if(!jQuery.tipsy)
{
	$.ajax({
		url: urlStaticFiles + 'js/tipsy.js',
		dataType: 'script',
		async:   false 
	});
}

function showMySession()
{
	showLoadingSpinner(loadingDiv, null);
	try
	{
		var sessionUSID= mySessionsGetSessionUSID();
		if(sessionUSID != 'noSessions' && sessionUSID != '' && sessionUSID != null)
		{
			var str= 'sessionUSID=' + sessionUSID;
			$.post('/sessions/show/', str, function(data){
				try
				{
					//if(data.search('<error>.*?</error>') <= -1)
					if($(data).find('error').length <= 0)
					{
						$('#concentDiv').html($(data).find('htmlData').text());
						prepareForNewGrid($('#contentDiv'));
						//set tipsy
						$('#tableStatus').tipsy({fade:true, gravity: 's'});
						$('.toolTip').tipsy({fade:true, gravity: 's', delayIn: 1500});
						hideLoadingSpinner(loadingDiv);
						hasTableBeenSaved= true;
						masterFormString = $('#form').serialize();
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
			var obj= $('#tableStatus');
			obj.attr('src', urlStaticFiles + 'icons/table_not_saved.png');
			obj.attr('title', 'Current showing table has been modified since retrieving it from the server.');
			hasTableBeenSaved= false;
		}
	}
	else
	{
		if(!hasTableBeenSaved)
		{
			var obj= $('#tableStatus');
			obj.attr('src', urlStaticFiles + 'icons/table_saved.png');
			obj.attr('title', 'Current showing table has not been modified since retrieving it from the server.');
			hasTableBeenSaved= true;
		}
	}
}

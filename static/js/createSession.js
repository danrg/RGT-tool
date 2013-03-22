var urlStaticFiles = '/static/';
var loadingDiv = $('#wrap');

//load other needed scripts
if (typeof showColMenu != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/gridTableGeneralFunctions.js',
		dataType: 'script',
		async:   false
	});
}

function showGridSessionSelection(){
	showLoadingSpinner($('#createSessionBasedOnGrid'), null);
	try
	{
		var gridUSID = $("#gridSessionSelection option:selected").val();
		if (gridUSID != "noGrids" && gridUSID != "" && gridUSID != null)
		{
			var str = 'viewMode=all&writeMode=read&gridUSID=' + gridUSID;
			$.post('/grids/show/', str, function (data) {
				try
				{
					if($(data).find('error').length <= 0)
					{
						$('#createSessionBasedOnGrid').html($(data).find('htmlData').text());
						prepareForNewGrid($('#createSessionBasedOnGrid'));
						//calculateTotalWeight($('#createSessionBasedOnGrid').find('table'));
						hideLoadingSpinner($('#createSessionBasedOnGrid'));
					}
					else
					{
						hideLoadingSpinner($('#createSessionBasedOnGrid'));
						showMessageInDialogBox($(data).find('error').text()); //function from gridNavigation
						//$('#createSessionDialog').html('<p>' + $(data).find('error').text() + '</p>')
						//$('#createSessionDialog').dialog('open');
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
	        $('#createSessionBasedOnGrid').html('<p style="padding:50px;text-align: center;"> Select a grid from the dropdown menu.</p>');
	        hideLoadingSpinner($('#createSessionBasedOnGrid'));
	    }
	}
	catch(err)
	{
		hideLoadingSpinner($('#createSessionBasedOnGrid'));
		console.log(err);
	}
}

function createSession()
{
	showLoadingSpinner(loadingDiv, 'Creating...');
	try
	{
        var showResults = $('input:radio[name=showResults]:checked').val();
        var gridUSID = $("#gridSessionSelection option:selected").val();
		var sessionName = $("#sessionNameInputBox").val();
        var str = 'gridUSID=' + gridUSID + '&sessionName=' + sessionName + '&showResults=' + showResults;
		var jqxhr = $.post('/sessions/create/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					//clear the div with the table
					$('#createSessionBasedOnGrid').html('');
					//clear the name of the grid
					$('#sessionNameInputBox').val('');
					$('#createSessionBasedOnGrid').html('<p style="padding:50px;text-align: center;"> Select a grid from the dropdown menu.</p>');
					//$('#createSessionDialog').html('<p> Session has been created </p>')
					//$('#createSessionDialog').dialog('open');
					hideLoadingSpinner(loadingDiv);
					$("#gridSessionSelection").val('0');
					showMessageInDialogBox($(data).find('htmlData').text(), function(){
						//redirect to the session page
						window.location.href= "/sessions/";
					}); //function from dialogbox.js
					
				}
				else
				{
					//$('#createSessionDialog').html('<p>' + $(data).find('error').text() + '</p>')
					//$('#createSessionDialog').dialog('open');
					hideLoadingSpinner(loadingDiv);
					showMessageInDialogBox($(data).find('error').text()); //function from gridNavigation
				}
			}
			catch(err)
			{
				hideLoadingSpinner(loadingDiv);
				console.log(err);
			}
		});
		//in case we have an error 500 or something like that the loader should still be closed
		jqxhr.error(function(){
			hideLoadingSpinner(loadingDiv);
			showMessageInDialogBox("Unknown server error");
		});
	}
	catch(err)
	{
		hideLoadingSpinner(loadingDiv);
		console.log(err);
	}
}
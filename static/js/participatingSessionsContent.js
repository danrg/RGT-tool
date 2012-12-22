function sendResponse()
{
	showLoadingSpinner($('#wrap'), 'Please wait...')
	try
	{
		var sessionUSID= participatingGetSessionUSID(); //function is from participatingSession.js
		var iteration= $.trim($('#participantSessionIteration').text());
		var table= getGridTable($('#participatingSessionResponseGridForm'));
		var nAlternatives= getNumberOfAlternatives(table);
		var nConcerns= getNumberOfConcerns(table);
		var form= $('#participatingSessionResponseGridForm');
		var strD= '';
		//serialize the disabled inputs
		form.find('input:disabled').each(function(){
			strD = strD + '&' + $(this).attr('name') + '=' + $(this).val();
		});
		var str=  'nConcerns=' + nConcerns + '&nAlternatives=' + nAlternatives + '&iteration=' + iteration + '&gridType=response&sessionUSID=' + sessionUSID + '&' + form.serialize() + strD;
		//double function is needed here because we want access to sessionUSID
		var callBack= function(sessionID){

			return function(data){
				try
				{
					if($(data).find('error').length <= 0)
					{
						var dateTime = $(data).find('dateTime').text();
						$('#responseStatusA').attr('class', 'green');
						$('#responseStatusSpan').text('Response was sent at: ' + dateTime);
						if($(data).find('extra').find('nResponses').length >= 1)
						{
							$('#nReceivedResponses').text($(data).find('extra').find('nResponses').text());
						}
						hideLoadingSpinner($('#wrap'));
						showMessageInDialogBox('Response was sent.');
						removePendingSessionResponse(sessionID); //function from participatingSessions.js
						//$('.participatingSessionsResponseHighlight').effect('highlight', {color: '#AFDCEC'}, 1500);
					}
					else
					{
						hideLoadingSpinner($('#wrap'));
						showMessageInDialogBox($(data).find('error').text());
					}
				}
				catch(err)
				{
					console.log(err);
					hideLoadingSpinner($('#wrap'));
				}
			}
		}

		$.post('/sessions/respond/', str, callBack(sessionUSID));
	}
	catch(err)
	{
		console.log(err);
		hideLoadingSpinner($('#wrap'));
	}
}

function getResponseFromIteration(iteration)
{
	showLoadingSpinner($('#wrap'), 'Please wait...')
	var currentIteration = false;
	try
	{

		var sessionUSID= participatingGetSessionUSID(); //function is from participatingSession.js
		if(iteration == null || iteration == '')
		{
			iteration= $('#responseSelection option:selected').val();
		}
		if(iteration != null && iteration != 'null')
		{
			if(iteration == 'current')
			{
				currentIteration = true;
				iteration= $('#participantSessionIteration').text();
			}
			str= 'sessionUSID=' + sessionUSID + '&iteration=' + iteration;
			$.post('/sessions/response/', str, function(data){
				try
				{
					if($(data).find('error').length <= 0)
					{
						$('#participationSessionsContentDiv').html($(data).find('htmlData').text());
						if (currentIteration){
							$('#participatingSessionCurrentSessionGridHeader').html('Session Grid of Current Iteration');
						} else {
							$('#participatingSessionCurrentSessionGridHeader').html('Session Grid of Iteration '+iteration);
						}
						$('#participationSessionsContentGridsDiv').find('.gridTrableContainerDiv').each(function(){
							prepareForNewGrid($(this));	
						});
						hideLoadingSpinner($('#wrap'));
					}
					else
					{
						hideLoadingSpinner($('#wrap'));
						showMessageInDialogBox($(data).find('error').text());
					}
				}
				catch(err)
				{
					console.log(err);
					hideLoadingSpinner($('#wrap'));
				}
			})
		}
		else
		{
			hideLoadingSpinner($('#wrap'));
		}
	}
	catch(err)
	{
		console.log(err);
		hideLoadingSpinner($('#wrap'));
	}
}

function sessionsGetSessionUSID()
{
    return $("#participatingSessionSelect option:selected").val();
}

function sessionsShowResults()
{
    var selectedOption = $('#resultSelection option:selected');
    var iteration= selectedOption.val();
    if (iteration > 0) {
        var sessionUSID= sessionsGetSessionUSID();
        var str= 'sessionUSID=' + sessionUSID + '&iteration=' + iteration;
        //get the result tables
        $.post('/sessions/responseResults/', str, function(data){
            if($(data).find('error').length <= 0)
            {
                $('#sessionsContentResultDiv').html($(data).find('htmlData').text());
                $('#clearResultsButton').show();
            }
            else
            {
                clearResults();
                showMessageInDialogBox($(data).find('error').text());
            }
        });
    }
}

function clearResults() {
    $('#sessionsContentResultDiv').empty();
    $('#clearResultsButton').hide();
    clearRatioResultCharts(); //function from resultRatingWeightTables.js
}
var urlStaticFiles= '/static/';
var intervalId= null;
var participantTableRefreshTime= 900000; //15 min refresh time

if( typeof createDendogram != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/svgDendogram.js',
		dataType: 'script',
		async:   false 
	});
}

if( typeof createSvgMenu != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/svgMenu.js',
		dataType: 'script',
		async:   false 
	});
}



//function definitions

/**
 * Initialize anything that needs to be done after the content page has loaded
 */
function initializeMySessionsContent()
{
	//set the refresh time of the participant table
	if(intervalId != null)
	{
		clearInterval(intervalId);
	}
	intervalId= setInterval(function(){refreshParticipantTable()}, participantTableRefreshTime);
}

/**
 * check if the session is in the R/W, A/C or Invitation state, if so refresh the participating users
 */
function refreshParticipantTable()
{
	var sessionStatus= $('#currentIterationStatus').html();
	if(sessionStatus == 'Invitation' || sessionStatus == 'A/C' || sessionStatus == 'R/W')
	{
		getParticipantPage();
	}
}

function startSession()
{
	showLoadingSpinner($('#wrap'), 'Please wait...');
	try
	{
		var str= 'sessionUSID=' + mySessionsGetSessionUSID() + '&newState=check'; //mySessionsGetSessionId is from mySessions.js
		$.post('/sessions/state/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					$('#' + getContentDivId()).html($(data).find('htmlData').text());
					prepareForNewGrid($('#contentDiv'));
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
				hideLoadingSpinner($('#wrap'));
				console.log(err);
			}
		});
	}
	catch(err)
	{
		console.log(err);
		hideLoadingSpinner($('#wrap'));
	}
}

function requestAlternativeConcerns()
{
	showLoadingSpinner($('#wrap'), 'Please wait...');
	try
	{
		var str= 'sessionUSID=' + mySessionsGetSessionUSID() + '&newState=waitingForAltAndCon'; //mySessionsGetSessionId is from mySessions.js
		$.post('/sessions/state/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					$('#' + getContentDivId()).html($(data).find('htmlData').text());
					prepareForNewGrid($('#contentDiv'));
					hideLoadingSpinner($('#wrap'));
				}
				else
				{
					hideLoadingSpinner($('#wrap'));
					//alert($(data).find('error').text());
					showMessageInDialogBox($(data).find('error').text());
				}
			}
			catch(err)
			{
				hideLoadingSpinner($('#wrap'));
				console.log(err);
			}
		});
	}
	catch(err)
	{
		console.log(err);
		hideLoadingSpinner($('#wrap'));
	}
}

function requestRatings()
{
	showLoadingSpinner($('#wrap'), 'Please wait...');
	try
	{
		var str= 'sessionUSID=' + mySessionsGetSessionUSID() + '&newState=waitingForWeightsAndRatings'; //mySessionsGetSessionId is from mySessions.js
		$.post('/sessions/state/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					$('#' + getContentDivId()).html($(data).find('htmlData').text());
					prepareForNewGrid($('#contentDiv'));
					hideLoadingSpinner($('#wrap'));
				}
				else
				{
					hideLoadingSpinner($('#wrap'));
					//alert($(data).find('error').text());
					showMessageInDialogBox($(data).find('error').text());
				}
			}
			catch(err)
			{
				console.log(err);
				hideLoadingSpinner($('#wrap'));
			}
		});
	}
	catch(err)
	{
		console.log(err);
		hideLoadingSpinner($('#wrap'));
	}
}

function finishSession() {
	
	showLoadingSpinner($('#wrap'), 'Please wait...');
	try
	{
		var str= 'sessionUSID=' + mySessionsGetSessionUSID() + '&newState=finish'; //mySessionsGetSessionUSID is from mySessions.js
		$.post('/sessions/state/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					$('#' + getContentDivId()).html($(data).find('htmlData').text());
					prepareForNewGrid($('#contentDiv'));
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
		});
	}
	catch(err)
	{
		console.log(err);
		hideLoadingSpinner($('#wrap'));
	}
}

function saveSessionGrid()
{
	hideLoadingSpinner($('#mySessionsResultDendrogramDiv'));
	try
	{
		var form= $('#sessionGridDiv').find('form');
		var table= getGridTable($('#sessionGridDiv'));
		var iteration= $('#iteration').text();
		str= 'nConcerns=' + getNumberOfConcerns(table) + '&nAlternatives='+ getNumberOfAlternatives(table) + '&gridType=session' + '&iteration=' + iteration + '&sessionUSID='+ mySessionsGetSessionUSID() + '&' + form.serialize();
		$.post('/grids/update/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					masterFormString = $('#form').serialize();
					isTableSaved();
					showMessageInDialogBox($(data).find('htmlData').text());
					hideLoadingSpinner($('#mySessionsResultDendrogramDiv'));
				}
				else
				{
					hideLoadingSpinner($('#mySessionsResultDendrogramDiv'));
					showMessageInDialogBox($(data).find('error').text());
				}
			}
			catch(err)
			{
				console.log(err);
				hideLoadingSpinner($('#mySessionsResultDendrogramDiv'));
			}
		});
	}
	catch(err)
	{
		console.log(err);
		hideLoadingSpinner($('#mySessionsResultDendrogramDiv'));
	}
}

function finishCurrentRequest()
{
	showLoadingSpinner($('#wrap'), 'Please wait...');
	try
	{
		var str= 'sessionUSID=' + mySessionsGetSessionUSID() + '&newState=check'; //mySessionsGetSessionId is from mySessions.js
		$.post('/sessions/state/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					$('#' + getContentDivId()).html($(data).find('htmlData').text());
					prepareForNewGrid($('#contentDiv'));
					hideLoadingSpinner($('#wrap'));
				}
				else
				{
					hideLoadingSpinner($('#wrap'));
					//alert($(data).find('error').text());
					showMessageInDialogBox($(data).find('error').text());
				}
			}
			catch(err)
			{
				console.log(err);
				hideLoadingSpinner($('#wrap'));
			}
		});
	}
	catch(err)
	{
		console.log(err);
		hideLoadingSpinner($('#wrap'));
	}
}

function mySessionsShowResults()
{
	var selectedOption = $('#mySessionsContentSessionIterationSelect option:selected');
	var iteration= selectedOption.val();
	if (iteration > 0) {
		var sessionUSID= mySessionsGetSessionUSID();
		var str= 'sessionUSID=' + sessionUSID + '&iteration=' + iteration;
		//get the result tables
		$.post('/sessions/results/', str, function(data){
			if($(data).find('error').length <= 0)
			{
				//get the dendrogram for the result only if the state of the result
				//is different from alternatives and concerns
				if (selectedOption.attr('class') != 'waitingForAltAndCon') {
					showSessionDendrogram(iteration, 'mySessionsResultDendrogramDiv');
				} else {
					$('#mySessionResultsDendrogram').hide();
				}
				$('#mySessionsContentResultDiv').html($(data).find('htmlData').text());
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

/**
 * 
 * @param iteration if not present, the iteration selected in the mySessionsContentSessionIterationSelect combo box will be used. Iteration of -1 represents the current iteration
 * @param divId if not present, the mySessionDendrogramDiv div will be used
 */
function showSessionDendrogram(iteration, divId)
{
	var dendrogramDiv= null;
	if(divId != null && divId != '')
	{
		dendrogramDiv= divId;
	}
	else
	{
		dendrogramDiv= 'mySessionDendrogramDiv';
	}
	showLoadingSpinner($('#' + dendrogramDiv));
	try
	{
		if(iteration == null || iteration == '')
		{
			iteration= $('#mySessionsContentSessionIterationSelect option:selected').val();
		}
		//in case the iteration is not specified display the current session
		if(iteration <=  0)
		{
			iteration= -1;
		}
		var sessionUSID= mySessionsGetSessionUSID();
		var str= 'sessionUSID=' + sessionUSID + '&iteration=' + iteration;
		$.post('/sessions/dendrogram/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					$('#'+dendrogramDiv).parent('div').show();
					if (iteration > 0) {
						$('#mySessionResultsDendrogramTitleIteration').text(iteration);
					}
					clearSvgImg(dendrogramDiv);
					createDendogram(dendrogramDiv, data);
					//create the menu for the svg
					createSvgMenu($('#' + dendrogramDiv), null);
					hideLoadingSpinner($('#' + dendrogramDiv));
				}
				else
				{
					$('#'+dendrogramDiv).parent('div').hide();
					if ((iteration != $('#iteration')) && (iteration > 0)) {
						showMessageInDialogBox('The dendrogram of iteration <b style="color: red;">'+iteration+'</b> cannot be generated. '+$(data).find('error').text());
					} else {
						showMessageInDialogBox($(data).find('error').text());
					}
					hideLoadingSpinner($('#' + dendrogramDiv));
				}
			}
			catch(err)
			{
				hideLoadingSpinner($('#' + dendrogramDiv));
				console.log(err);
			}
		});
	}
	catch(err)
	{
		hideLoadingSpinner($('#' + dendrogramDiv));
		console.log(err);
	}
}

function getParticipantPage()
{
	showLoadingSpinner($('#sessionParticipants'), 'Please wait...');
	try
	{
		//request for the user panel
		var str= 'sessionUSID=' + mySessionsGetSessionUSID(); //mySessionsGetSessionId is from mySessions.js
		$.post('/sessions/participants/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					hideLoadingSpinner($('#sessionParticipants'));
					$('#sessionParticipants').html($(data).find('htmlData').text());
				}
				else
				{
					hideLoadingSpinner($('#sessionParticipants'));
					showMessageInDialogBox($(data).find('error').text());
				}
			}
			catch(err)
			{
				hideLoadingSpinner($('#sessionParticipants'));
				console.log(err);
			}
		});
	}
	catch(err)
	{
		hideLoadingSpinner($('#sessionParticipants'));
		console.log(err);
	}
}

function getSessionGrid()
{
	showLoadingSpinner($('#sessionGridDiv'), 'Please wait...');
	try
	{
		var str= 'sessionUSID=' + mySessionsGetSessionUSID();
		$.post('/sessions/sessionGrid/', str, function(data){
			
			try
			{
				if($(data).find('error').length <= 0)
				{
					$('#form').html($(data).find('htmlData').text());
					prepareForNewGrid($('#contentDiv'));
					hideLoadingSpinner($('#sessionGridDiv'));
				}
				else
				{
					hideLoadingSpinner($('#sessionGridDiv'));
					showMessageInDialogBox($(data).find('error').text());
				}
			}
			catch(err)
			{
				hideLoadingSpinner($('#sessionGridDiv'));
				console.log(err);
			}
		});
	}
	catch(err)
	{
		hideLoadingSpinner($('#sessionGridDiv'));
		console.log(err);
	}
}

function clearResults() {
	$('#mySessionsResultDendrogramDiv').empty();
	$('#mySessionsContentResultDiv').empty();
	$('#mySessionResultsDendrogram').hide();
	$('#clearResultsButton').hide();
	clearRatioResultCharts(); //function from resultRatingWeightTables.js
}
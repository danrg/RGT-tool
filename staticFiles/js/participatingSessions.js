var loadingDiv= $('#wrap');

function joinSession()
{
	showLoadingSpinner(loadingDiv, 'Joining please wait...');
	try
	{
		invitationKey= $('#invitationKeyInput').val();
		str= 'invitationKey=' + invitationKey;
		$.post('/sessions/join/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					//$('#participatingSessionsDialog').html('<p>' + $(data).find('htmlData').text() + '</p>');
					//$('#participatingSessionsDialog').dialog('open');
					showMessageInDialogBox($(data).find('htmlData').text()); //function from gridNavigation
					
					//if this is the first session add an empty option in the combobox
					if($('#participatingSessionSelect option').length <= 1)
					{
						$('#participatingSessionSelect option:last').after('<option value="noSession" ></option>');
					}
					//add the new session to the comboBox
					var xmlNode= $(data).find('extra>comboxData>element');
					if(xmlNode.length >= 1)
					{
						xmlNode.each(function(){
							$('#participatingSessionSelect option:last').after('<option value="' + $(this).find('value').text() + '" >' + $(this).find('display').text() + '</option>' );
						})
						$('#noSessionOption').remove();
					}
					//clear the input field of the key
					$('#invitationKeyInput').val('');
					hideLoadingSpinner(loadingDiv);
				}
				else
				{
					//var errorDescription= $(data).find('error').text();
					//$('#participatingSessionsDialog').html('<p>' + errorDescription + '</p>');
					//$('#participatingSessionsDialog').dialog('open');
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
	}
	catch(err)
	{
		hideLoadingSpinner(loadingDiv);
		console.log(err);
	}
}

function showParticipatingSessionDetails()
{
	showLoadingSpinner(loadingDiv, 'Please wait...');
	try
	{
		var sessionUSID= $('#participatingSessionSelect option:selected').val();
		if(sessionUSID != null && sessionUSID != 'noSession' && sessionUSID != '' )
		{	
			var str= 'sessionUSID=' + sessionUSID;
			$.post('/sessions/participate/', str, function(data){
				try
				{
					if($(data).find('error').length <= 0)
					{
						$('#participatingSessionContentDiv').html($(data).find('htmlData').text());
						if($('#participatingSessionGridDiv').find('table').length >= 1)
						{
							prepareForNewGrid($('#participatingSessionGridDiv'));
							prepareForNewGrid($('#participatingSessionGridAnswerDiv'));
						}
						hideLoadingSpinner(loadingDiv);
					}
					else
					{
						//alert($(data).find('error').text());
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

//get the session id of the information about a session the user is current seeing
function participatingGetSessionUSID()
{
	return $('#participatingSessionSelect option:selected').val();
}

//function used in pendingResponses.html
function openSession(sessionUSID)
{
	$('#participatingSessionSelect').find('option[value= "' + sessionUSID + '"]').attr('selected', true);
	showParticipatingSessionDetails();
}
var urlStaticFiles= '/static/';
var loadingDiv= $('#wrap');
	
//load needed scripts
if( typeof showColMenu != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/gridTableGeneralFunctions.js',
		dataType: 'script',
		async:   false 
	});
};

function prepareGrid()
{
	prepareForNewGrid($('#gridData').find('#gridDiv').find('table'));
}

function createGrid()
{
	showLoadingSpinner(loadingDiv, 'Please wait...');
	try
	{
		var table= $('#gridData').find('#gridDiv').find('table');
		var str= 'nAlternatives=' + getNumberOfAlternatives(table) + '&nConcerns=' + getNumberOfConcerns(table) + '&tableOnly=true&'+ $('#form').serialize();
		var error= '';
		$.post('/grids/create/', str, function(data){
			try
			{
				if($(data).find('error').length <= 0)
				{
					$('#gridName').val('');
					hideLoadingSpinner(loadingDiv);
					$('#gridData').html($(data).find('htmlData').text());
					console.log(data);
					//$('#gridCreationResultDiv').html('<p>Grid was created</p>');
					prepareGrid();
					showMessageInDialogBox('Grid was created.');
					
				}
				else
				{
					hideLoadingSpinner(loadingDiv);
					showMessageInDialogBox($(data).find('error').text()); //function from gridNavigation 
					//$('#createMyGridsDialog').html('<p>' + $(data).find('error').text() + '</p>');
					//$('#createMyGridsDialog').dialog('open');
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

function isTableSaved() {
	return false;
}
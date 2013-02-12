var urlStaticFiles= '/static/';
var hasTableBeenSaved= true;
var masterFormString = '';
var loadingDiv= $('#wrap');
var isGridCompleteFlag = false;

//load other javascript needed for the showMyGrids.html
if( typeof showColMenu != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/gridTableGeneralFunctions.js',
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

if( typeof createDendogram != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/svgDendogram.js',
		dataType: 'script',
		async:   false 
	});
}

//function used to get a grid from the db and display it to the user
function showMyGrid(reload)
{
	var gridUSID;
	if (!reload){
		gridUSID = $("#showGridSelection option:selected").val();
	} else {
		gridUSID = $("#gridUSID").val();
	}
	var gridName= $("#showGridSelection option:selected").text();
	if(gridUSID != "noGrids" && gridUSID != "" && gridUSID != null)
	{
		showLoadingSpinner(loadingDiv, null);
		try
		{
			var str= 'checkTable=true&viewMode=all&writeMode=write&gridUSID=' + gridUSID;
			$.post('/grids/show/', str, function(data){
				
				try
				{
					//clear the information div
					$("#informationDiv").html('');
					
					if($(data).find('error').length <= 0)
					{
						$('#results').show();
						if($('.tableOptions').is(':hidden'))
						{
							$('.tableOptions').show();
						}
						
						$("#results").html($(data).find('htmlData').text());
						prepareForNewGrid($('#results'));	//this function is from gridTableGeneralFunctions.js
						
						//calculate total weight
						calculateTotalWeight($('#results'));
									
						//set table status as matching with the db 
						hasTableBeenSaved= true;
									
						//make the form string that represent the saved table in db
						masterFormString= $("#form").serialize();
						
						isGridComplete();
									
						//set tipsy
						initiateGridTableToolTip($('#results'))
						
						//clear the histogram
//						if($('#dendogramDiv').find('img').is('#dendogramImage'))
//						{
//							$('#dendogramDiv').find('#dendogramImage').remove();
//						}
						clearSvgImg('dendogramDiv');
						
						// show the grid name in the box
						$('#gridName').val(gridName);
						$('#gridNameDiv').show();
						$('#gridUSID').val(gridUSID);
						
						hideLoadingSpinner(loadingDiv);
					}
					else
					{
						$('#myGridsDialog').html('<p>' +  $(data).find('error').text() + '</p>');
						$('#myGridsDialog').dialog('open');
						hideLoadingSpinner(loadingDiv);
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
};
		
function deleteMyGrid(){		
	
	//var str= 'grid='+$("#showGridSelection option:selected").val();
	var gridUSID = $("#gridUSID").val();
	var str = 'gridUSID='+gridUSID;
	// first display an confirmation dialog to the user asking if he is sure that he wants to delete the grid
	dialogDiv= getDialogDiv();// function if from layout.html
	dialogDiv.html('<p>You are about to delete a grid, do you really want to do that?</p>');
	dialogDiv.dialog({
		title: 'Delete grid?',
		resizable: false,
		height:140,
		modal: true,
			buttons: {
			"Delete grid": function() {
				//when the user confirms he wants to delete the grid, send the request to the server
				$( this ).dialog( "close" );
				showLoadingSpinner(loadingDiv, 'Deleting...');
				try
				{
					$.post('/grids/delete/', str, function(data){
						try
						{
							if($(data).find('error').length <= 0)
							{
								$('#showMyGridsTableOptions').hide();
								$("#showGridSelection option[value='"+gridUSID+"']").remove();
								$("#showGridSelection").selectedIndex= 0;
								if ($("#showGridSelection option").length <= 1) {
									$("#showGridSelection option:selected").text("no grids available");
									$("#information").html('<p>You do not have any grids yet. Please <a href="/grid/createMyGridPage/">create</a> one!</p>');
								}
								$("#results").html('');
								$("#gridName").val('');
								$("#gridUSID").val('');
								$("#gridNameDiv").hide();
								//clear the histogram
//								if($('#dendogramDiv').find('img').is('#dendogramImage'))
//								{
//									$('#dendogramDiv').find('#dendogramImage').remove();
//								}
								clearSvgImg('dendogramDiv');
								$('#results').hide();
								$('#dendrogram').hide();
								hideLoadingSpinner(loadingDiv);
								showMessageInDialogBox('Grid was deleted.');
							}
							else
							{
								//$('#myGridsDialog').html('<p>' + $(data).find('error').text() + '</p>');
								//$('#myGridsDialog').dialog('open');
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
					console.log(err)
				}
			},
			Cancel: function() {
				hideLoadingSpinner(loadingDiv);
				$( this ).dialog( "close" );
			}
		}
	});
};

//check if the table is saved
function isTableSaved()
{
	if(masterFormString != $("#form").serialize())
	{
		if(hasTableBeenSaved)
		{
			changeTableSaveStatusIcon($('#results'), false);
			setGridTableSaveStatusToolTip($('#results'), 'Current showing table has been modified since retrieving it from the server.');
			hasTableBeenSaved= false;
			// this is needed here because in order to generate the dendogram, we use the values
			// that are stored, and if the table is saved which means that the values shown are
			// the same as in the database, then we can generate
			isGridComplete();
		}
	}
	else
	{
		if(!hasTableBeenSaved)
		{
			changeTableSaveStatusIcon($('#results'), true);
			setGridTableSaveStatusToolTip($('#results'), 'Current showing table has not been modified since retrieving it from the server.');
			hasTableBeenSaved= true;
			isGridComplete();
		}
	}
}

function saveGrid()
{
	showLoadingSpinner(loadingDiv, 'Saving...');
	try{
		var formString= $("#form").serialize();
		var table= getGridTable($('#results'));
		var gridUSID = $("#gridUSID").val();
		var gridName= $("#gridName").val();
		var str= 'gridUSID=' + gridUSID + '&gridName=' + gridName + '&nAlternatives=' + getNumberOfAlternatives(table) + '&nConcerns=' + getNumberOfConcerns(table) + '&' + formString;
		$.post('/grids/update/', str, function(data)
		{
			try
			{
				if($(data).find('error').length <= 0)
				{
					hideLoadingSpinner(loadingDiv);
					showMessageInDialogBox($(data).find('htmlData').text()); //function is from layout.html
					masterFormString= formString;
					$("#showGridSelection option[value='"+gridUSID+"']").text(gridName);
					//set the table to save
					isTableSaved();
				}
				else
				{
					hideLoadingSpinner(loadingDiv);
					showMessageInDialogBox($(data).find('error').text()); //function from layout.html
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

function getDendogram()
{
	showLoadingSpinner($('#dendogramDiv'));
	try
	{
		var gridUSID = $("#gridUSID").val();
		var str = 'gridUSID=' + gridUSID;
		$.post('/grids/dendrogram/', str, function(data)
				{
					try
					{
						if($(data).find('error').length <= 0)
						{
							$('#dendrogram').show();
							clearSvgImg('dendogramDiv');
							// extra the svg data from the xml file
							var svg= $.parseXML($(data).find('svgData').text());
							createDendogram('dendogramDiv', svg);
							createSvgMenu($('#dendogramDiv'), {saveItemAs: true, saveItemAsUrl: '/grids/download/dendrogram/', saveItemAsArguments:{gridUSID: gridUSID}});
							//createSvgMenu($('#dendogramDiv'), null);
							$('#dendrogramTitle').text('Dendrogram of grid: '+ $('#gridName').val());
							hideLoadingSpinner($('#dendogramDiv'));
						}
						else
						{
							hideLoadingSpinner($('#dendogramDiv'));
							console.log($(data).find('error').text());
							showMessageInDialogBox($(data).find('error').text());// function is from layout.html	
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
		hideLoadingSpinner($('#dendogramDiv'));
		console.log(err)
	}
}

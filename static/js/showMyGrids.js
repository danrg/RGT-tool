var urlStaticFiles = '/static/';
var hasTableBeenSaved = true;
var masterFormString = '';
var loadingDiv = $('#wrap');
var isGridCompleteFlag = false;

//load other javascript needed for the showMyGrids.html
if (typeof showColMenu != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/gridTableGeneralFunctions.js',
		dataType: 'script',
		async:   false
	});
}

if (typeof createSvgMenu != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/svgMenu.js',
		dataType: 'script',
		async:   false
	});
}

if (typeof createDendogram != 'function')
{
	$.ajax({
		url: urlStaticFiles + 'js/svgDendogram.js',
		dataType: 'script',
		async:   false
	});
}

function hideImage()
{
    $('#dendrogram').hide();
}

function adjustWeights()
{
    $('#wContainer').html("");
    var table = getGridTable($('#results'));
    var numConcerns = getNumberOfConcerns(table);
    var dummyConStr = "#concern_";
    var dummyWeightStr = "#weight_concern";
    var dummySpanStr = "span_concern";
    var dummySpan = "<span id='";
    var dummyP = "<p id='"
    var dummyPStr = "pConcern"

    for(var i=1; i<=numConcerns; i++)
    {
        dummySpan = "<span id='";
        dummyP = "<p id='"
        var dummyConStr2 = dummyWeightStr + i.toString();
        var dummySpan2 = dummySpan + dummySpanStr + i.toString() + "'> " + Math.round($(dummyConStr2).val()) + "</span>";
        var dummyP2 = dummyP + dummyPStr + i.toString() + "'>&nbsp;&nbsp;" + Math.round($(dummyConStr2).val()) + "</p>";
        var cName = dummyConStr + i.toString() + "_left";
        var cName2 = "<p>" + $(cName).val() + "</p>";
        $('#wContainer').append(cName2);
        $('#wContainer').append(dummySpan2);
        $('#wContainer').append(dummyP2);
    }

     $( "#wContainer > span" ).each(function() {
      // read initial values from markup and remove that
      var value = parseInt( $( this ).text(), 10 );
      $(this).empty().slider({
        value: value,
        range: "min",
        min: 1,
        max: 100-(numConcerns-1),
        animate: true,
        step: 1,
        slide: function(event, ui) {

            var clicked = "#" + $(this).attr('id');
            pClicked = clicked;
            pClicked = pClicked.replace("span", "pConcern");
            pClicked = pClicked.replace("_concern", "");

            $(pClicked).text("\xa0\xa0"+ui.value.toString());
        },
        stop: function( event, ui ) {
            for(var k=1; k<=numConcerns; k++)
            {
                var pDummy = "#pConcern" + k.toString();
                var spanDummy = "#span_concern" + k.toString();
                var wDummy = "#weight_concern" + k.toString();
                var clicked = "#" + $(this).attr('id');
                clicked = clicked.replace("span", "weight");
                if($(this).attr('id') != $(spanDummy).attr('id'))
                {
                    var val = $(spanDummy).slider("value");
                    $(spanDummy).slider("value", val-((ui.value-$(clicked).val())*($(spanDummy).slider("value")/(100-$(clicked).val()))));

                }
                $(pDummy).text($(spanDummy).slider("value").toString());
            }

            var total = 0;
            for(var i=1; i<=numConcerns; i++)
            {
                    var clicked = "#" + $(this).attr('id');
                    var spanDummy = "#span_concern" + i.toString();
                    if($(this).attr('id') != $(spanDummy).attr('id'))
                        total += $(spanDummy).slider("value");
                    else
                        total += ui.value;
            }

            if(total != 100)
            {
                if(total>100)
                {
                    var dif = total - 100;
                    for(var a=1; a<=numConcerns && dif>0; a++)
                    {
                        var spanDummy = "#span_concern" + a.toString();
                        if($(this).attr('id') != $(spanDummy).attr('id'))
                        {
                            if($(spanDummy).slider("value")>dif)
                            {
                                $(spanDummy).slider("value", $(spanDummy).slider("value")-dif);
                                dif = 0;
                            }
                        }

                    }
                }
                else
                {
                    var dif = 100 - total;
                    for(var b=1; b<=numConcerns && dif>0; b++)
                    {

                        var spanDummy = "#span_concern" + b.toString();
                        if($(this).attr('id') != $(spanDummy).attr('id'))
                        {
                            if($(spanDummy).slider("value")+dif<100)
                            {   $(spanDummy).slider("value", $(spanDummy).slider("value")+dif);
                                dif = 0;
                            }
                        }

                    }
                }
            }
            for(var j=1; j<=numConcerns; j++)
            {
                    var pDummy = "#pConcern" + j.toString();
                    var spanDummy = "#span_concern" + j.toString();
                    var wDummy = "#weight_concern" + j.toString();

                $(pDummy).text("\xa0\xa0"+$(spanDummy).slider("value").toString());
                $(wDummy).val($(spanDummy).slider("value"));

            }
            isTableSaved();
        }
      });
    });

    toggleAdjustWeights();
}

function toggleAdjustWeights() {
    $('#weightSlidersButton').toggle();
    $('#cancelWeightSliders').toggle();
    $('#weightSliders2').toggle();
    $('#reloadSavedGridButton').toggle();
    $('#deleteGrid').toggle();
    $('#results').toggle();
    $('#wContainer').toggle();
    $('#totalW').toggle();
}

function resetVisibilities() {
    $('#results').show();
    $('#weightSlidersButton').show();
    $('#totalW').hide();
    $('#wContainer').hide();
    $('#weightSliders2').hide();
    $('#similarityMatrix').hide();
    $('.resim').remove();
    clearSvgImg('dendogramDiv');
    $('#reloadSavedGridButton').show();
    $('#deleteGrid').show();
    $('#cancelWeightSliders').hide();
}

//function used to get a grid from the db and display it to the user
function showMyGrid(reload)
{
    if ($('#tabs').is(':hidden'))
    {
        $('#tabs').show();
    }
	var gridUSID;
	if (!reload) {
		gridUSID = $("#showGridSelection option:selected").val();
	} else {
		gridUSID = $("#gridUSID").val();
	}
	var gridName= $("#showGridSelection option:selected").text();
    showGrid(gridUSID, gridName);
}

function showGrid(gridUSID, gridName)
{
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
					$("#information").html('Select another grid:');

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
						initiateGridTableToolTip($('#results'));

						//clear the histogram
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
}

function getPCA()
{
    if(isGridValid())
    {
        showLoadingSpinner($('#pca'));
        try
        {
            var gridUSID = $("#gridUSID").val();
            var str = 'result.png?gridUSID=' + gridUSID;

            var img = $("<img class = 'resim'/>").attr('src', str).load(function() {
                if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                alert('broken image!');
                } else {
                 $("#pca").show();
                 $("#pcaResult").show();
                 $("#pcaResult").append(img);
                 hideLoadingSpinner($('#pca'));
                }
            });
        }
        catch(err)
        {
            hideLoadingSpinner($('#pca'));
            console.log(err);
        }
    }else
    {
        showMessageInDialogBox("Please add at least one more concern");
    }
}

function deleteMyGrid()
{
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
}

//check if the table is saved
function isTableSaved()
{
	if(masterFormString != $("#form").serialize())
	{
		if(hasTableBeenSaved)
		{
			changeTableSaveStatusIcon($('#results'), false);
			setGridTableSaveStatusToolTip($('#results'), 'Current showing table has been modified since retrieving it from the server.');
			hasTableBeenSaved = false;
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
    $('#reloadSavedGridButton').prop('disabled', hasTableBeenSaved);
    $('#saveButton').prop('disabled', hasTableBeenSaved);
    isGridComplete();
}

function saveGrid()
{
	showLoadingSpinner(loadingDiv, 'Saving...');
	try{
		var formString = $("#form").serialize();
		var table = getGridTable($('#results'));
		var gridUSID = $("#gridUSID").val();
		var gridName = $("#gridName").val();

		var str = 'gridUSID=' + gridUSID + '&gridName=' + gridName + '&nAlternatives=' + getNumberOfAlternatives(table) + '&nConcerns=' + getNumberOfConcerns(table) + '&' + formString;
		$.post('/grids/update/', str, function(data)
		{
			try
			{
				if ($(data).find('error').length <= 0)
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
    if(isGridValid())
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
            console.log(err);
        }
    }else
    {
        showMessageInDialogBox("Please add at least one more concern");
    }
}

function getMatrices()
{
    if(isGridValid())
    {
        showLoadingSpinner($('#similarityMatrix'));
        try
        {
            var gridUSID = $("#gridUSID").val();
            var str = 'gridUSID=' + gridUSID;
            $.post('/grids/similarity/', str, function(data)
                    {
                        try
                        {
                            if($(data).find('error').length <= 0)
                            {
                                $('#similarity').show();
                                $("#similarity").html($(data).find('htmlData').text());
                                hideLoadingSpinner($('#similarityMatrix'));
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
            hideLoadingSpinner($('#similarityMatrix'));
            console.log(err);
        }
    }else
    {
        showMessageInDialogBox("Please add at least one more concern");
    }
}

function isGridValid()
{
   var rowCount = $('.gridRow').length;
   return (rowCount > 1);
}

$(function() {
    $("#tabs").tabs();
});


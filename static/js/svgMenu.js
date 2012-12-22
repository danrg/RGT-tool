/**
 * Function that will create an menu for the svg.
 * This function requires that the svg tag be inside a wrap div tag without any elements inside it (excluding the svg tag),
 * the wrap div should positioned as relative so the menu can work properly.
 * @param wrapDiv the jquery obj representing the div
 * @param options Options is not mandatory. Available options are: showSaveButton: boolean, showClearButton: boolean, saveButtonFunction: function
 */
function createSvgMenu(wrapDiv, options)
{
	var svgDiv= wrapDiv.find('svg');
	var menuDiv= null;
	var saveButtonFunction= null;
	var showSaveButton= true;
	var showClearButton= true;

	//path of the images
	var saveButtonImg= '/static/icons/save.png';
	var clearButtonImg= '/static/icons/clear.png';

	var menuContent= '';
	
	//set the wrapDiv to relative
	wrapDiv.css({position:'relative'});
	
	//create the menu with the correct options
	{
		if(options == null)
		{
			options= {};
		}
		if('showSaveButton' in options)
		{
			if(options['showSaveButton'] == true)
			{
				menuContent+= '<img src="' + saveButtonImg + '" id="saveButtonImg" />';
			}
			else
			{
				showSaveButton= false;
			}
		}
		else
		{
			//default options is to add the button
			menuContent+= '<img src="' + saveButtonImg + '" id="saveButtonImg" />';
		}
		if('showClearButton' in options)
		{
			if(options['showClearButton'] == true)
			{
				menuContent+= '<img src="' + clearButtonImg + '" id="clearButtonImg" />'
			}
			else
			{
				showClearButton= false;
			}
		}
		else
		{
			//default is to shoe the button
			menuContent+= '<img src="' + clearButtonImg + '" id="clearButtonImg" />'
		}
		if('saveButtonFunction' in options)
		{
			if(options['saveButtonFunction'] != null)
			{
				saveButtonFunction= options['saveButtonFunction'];
			}
			else
			{
				saveButtonFunction= saveSvgAs;
			}
		}
		else
		{
			saveButtonFunction= saveSvgAs;
		}
	}
	
	//add the menu div inside the wrap div
	wrapDiv.append('<div style="position:absolute;">' + menuContent +  '</div>');
	
	menuDiv= wrapDiv.find('div');
	
	//add the functions to the images
	
	if(showClearButton)
	{
		var button= menuDiv.find('#clearButtonImg');
		button.click(function(){
			$(this).parent('div').parent('div').parent('div').hide();
		});
		button.hover(
				function(){
					$(this).css({'background-image': 'url(/static/icons/clear_hover.png)'});
				}, 
				function(){
					$(this).css({'background-image': 'url(/static/icons/clear.png)'});
				});
	}
	
	if(showSaveButton)
	{
		button= menuDiv.find('#saveButtonImg');
		button.click(function(){saveButtonFunction($(this))});
		button.hover(
				function(){
					$(this).css({'background-image': 'url(/static/icons/save_hover.png)'});
				}, 
				function(){
					$(this).css({'background-image': 'url(/static/icons/save.png)'});
				});
	}
	
	//set the position of the menu
	// -16 because the images height of the menu are 16px
	menuDiv.css({
		top: ((wrapDiv.height()/2) + (svgDiv.height()/2) - 16) + 'px',
		left: ((wrapDiv.width()/2) + (svgDiv.width()/2)) + 'px',
	});
//	menuDiv.position({
//		of: svgDiv,
//		at: 'right bottom',
//	});

	//set the functionality for the mouse enter and mouse leave
	wrapDiv.mouseenter(function(){
		$(this).find('div').show();
	});
	wrapDiv.mouseleave(function(){
		$(this).find('div').hide();
	});
	
	//hide the menu
	menuDiv.css({
		display: 'none'
	});

}

/**
 * Default function used to save the svg
 */
function saveSvgAs(imgObj)
{
	//the double function is used here so the tagData obj will be able to be used inside the function that will handle the post response
	var callBack= function(tagData)
	{
		
		return function(data)
		{
			var svg= getSvgFromDiv(tagData.parent('div').parent('div'));
			if($(data).find('error').length <= 0)
			{
				var modalDiv= getDialogDiv();
				modalDiv.html($(data).find('htmlData').text());
				var input = $('<input>').attr("type", "hidden").attr("name", "data").val(svg.toSVG()); 
				modalDiv.find('form').append($(input))
				$('#modalDialogBox').dialog({
			    	title: 'Download',
					resizable: false,
					width:400,
					modal: true,
					buttons: {'Download':function(){
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
	$.post('/grids/download/', '', callBack(imgObj));
}
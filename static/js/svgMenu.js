/**
 * Function that will create an menu for the svg.
 * This function requires that the svg tag be inside a wrap div tag without any elements inside it (excluding the svg tag),
 * the wrap div should positioned as relative so the menu can work properly.
 * @param wrapDiv the jquery obj representing the div
 * @param options Options is not mandatory. Available options are: showSaveButton: boolean, showClearButton: boolean, saveButtonFunction: function, 
 * saveItemAs: boolean, saveItemAsArguments: object with this format: {attribute: value, attribute: value, ...}, saveItemAsUrl: string
 * 
 * saveItemAsUrl: url that should be called to request something from the server and is mandatory when using saveItemAs: true
 * Observation: when using saveItemAsArguments the data will in that object will be sent to the server
 */
function createSvgMenu(wrapDiv, options)
{
	var svgDiv= wrapDiv.find('svg');
	var menuDiv= null;
	var saveButtonFunction= null;
	var showSaveButton= true;
	var showClearButton= true;
	var checkSaveButtonFunction= true;
	var saveItemAsArg= null;
	var saveItemAsUrl= null;

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
			//default is to show the button
			menuContent+= '<img src="' + clearButtonImg + '" id="clearButtonImg" />'
		}
		/* if saveItemAsArguments is true we will use the default saveItemAsArguments function, 
		 * else check if the saveButtonFunction is defined and if that fails, use
		 * the default function
		 */
		if('saveItemAs' in options && 'saveItemAsUrl' in options)
		{
			if(options['saveItemAs'] != null && options['saveItemAs'] == true && options['saveItemAsUrl'] != null)
			{
				saveItemAsUrl= options['saveItemAsUrl'];
				if ('saveItemAsArguments' in options)
				{
					saveItemAsArg= options['saveItemAsArguments'];
					checkSaveButtonFunction= false;
				}
			}
		}
		if('saveButtonFunction' in options && checkSaveButtonFunction)
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
		//check if we are going to use the saveDendogram function or not
		if(saveItemAsUrl != null)
		{
			button.click(function(){downloadItemAs($(this), saveItemAsUrl, saveItemAsArg)});
		}
		else
		{
			button.click(function(){saveButtonFunction($(this))});
		}
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
 * @param imgObj: object representing the <img> which was pressed to call this function
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
				var input = $('<input>').attr("type", "hidden").attr("name", "data").val(getSvgString(svg)); 
				modalDiv.find('form').append($(input))
				modalDiv.dialog({
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
	//get the download form
	$.post('/grids/download/', '', callBack(imgObj));
}

/**
 * Default function used to request a download of something from the server
 * @param imgObj object representing the <img> which was pressed to call this function
 * @param url url (string) that will be called by the post function
 * @param parameters obect with the arguments that should be passed to the server, format: { argumentName: value, argumentName: value, ......}
 */
function downloadItemAs(imgObj, url, parameters)
{
	//the double function is used here so the tagData obj will be able to be used inside the function that will handle the post response
	var callBack= function(imgObj2, url2, parameters2)
	{
		return function(data)
		{
			var svg= getSvgFromDiv(imgObj2.parent('div').parent('div'));
			if($(data).find('error').length <= 0)
			{
				
				var modalDiv= getDialogDiv();
				modalDiv.html($(data).find('htmlData').text());
				var form= modalDiv.find('form');
				var temp= null;
				if (parameters2 != null)
				{	
					for(attrib in parameters2)
					{
						temp= $('<input>').attr("type", "hidden").attr("name", attrib).val(parameters2[attrib]);
						form.append($(temp));
					}
				}
				form.attr('action', url2);
				modalDiv.dialog({
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
	//get the download form
	$.post('/grids/download/', '', callBack(imgObj, url, parameters));
}
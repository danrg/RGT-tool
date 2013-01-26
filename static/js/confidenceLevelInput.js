var urlStaticFiles= '/static/';
//load other javascript needed for the showMyGrids.html
if(!jQuery.svg)
{
	$.ajax({
		url: urlStaticFiles + 'js/jquerySvg/jquery.svg.js',
		dataType: 'script',
		async:   false 
	});
	
	$.ajax({
		url: urlStaticFiles + 'js/jquerySvg/jquery.svgfilter.js',
		dataType: 'script',
		async:   false 
	});
}

function dostuff()
{
	$('#testSvg').svg();
	var svg = $('#testSvg').svg('get');
	var text= svg.text(null, 30, 30, 'TEXT', {fill:'black', id:'svgText', fontSize: '16px'});
	svg.line(29, 29, 68, 29, {strokeWidth: 5, stroke:'black'})
	node = document.getElementById("svgText")
	//console.log(text.getComputedTextLength());
	//console.log(text);
	createRatingConfidenseLevelInput($('#testSvg2'), testR);
}

function testR(rowN, colN, rangeName, confidenceName)
{
	$('#t1').attr('value', rowN);
	$('#t2').attr('value', colN);
	$('#t3').attr('value', rangeName);
	$('#t4').attr('value', confidenceName);
}

/**
 * This function will create the interactive svg chart that will be used as the input for 
 * the rating and confidence level
 * @param div the div that should host the svg element (should be a jquery object)
 * @param returnFunction function that will be called when the user press one of the cells of the input chart. This function must be able to get 4 arguments: rowNumber (int), colNumber (int), range name (string), confidence level name (string)
 */
function createRatingConfidenseLevelInput(div, returnFunction)
{
	div.svg();
	var svg= div.svg('get');
	
	/* Settings */
	var chartYOffset= 5; //offset from the top element
	var cellCursor= 'pointer'; //this is a css property
	//general axis settings
	var axisFontName= 'Ariel';
	var axisFontColor= [0, 0, 0];
	//cell
	var minCellHeight= 20;
	var minCellWidth= 20;
	var cellExtraWidth= 5;
	var cellExtraHeight= 5;
	var cellLineThickness= 1;
	var cellColor= [222, 221, 245];
	//confidence level axi label
	var confidenceLevelWord= 'Confidence Level';
	var confidenceLevelFontSize= 16;
	var confidenceLevelLabelXOffset= 5; //offset of the confidence level label from the left element. In pixels
	//rating axi label
	var ratingWord= 'Rating';
	var ratingFontSize= 16;
	//confidence level ruler labels
	var confidenceLevels= ['very low', 'low', 'mid', 'high', 'very high'];
	var confidenceLevelLabelsXOffset= 10; //offset of the confidence level labels from the the confidence level label. In pixels
	//rating ruler label
	var ratings= ['1', '2', '3', '4', '5'];
	var ratingLabelYOffset= 10; //offset of the rating label from the bottom of the rating labels
	//ruler
	var rulerExtraHeight= 10;
	var rulerMarkerHeight= 7;
	var rulerMarkerLineWidth= 3;
	var rulerMarkerToLabelYOffset= 5; //the y offset from any label that is placed in alignment with the ruler
	var rulerLabelRatingMaxWidth= 50; //this set will have influence on the size of the cells as it is based on the size of the labels
	var rulerLabelConfidenceLevelMaxWidth= 60; // in pixels
	var rulerLineThickness= 3;
	var fontSize= 16; //in pixels
	var rulerFontName= 'Ariel';
	var rulerColor= [0, 0, 0];
	var rulerMarkerColor= [47, 47, 250];
	var rulerFontColor= [0, 0, 0];
	//arrow
	var arrowHeight= 12;
	var arrowWidth= 10;
	var arrowColor= [0, 0, 0];	
	//shadow filter
	var shadowFilterId1= 'shadowFilter1';
	var shadowFilterId2= 'shadowFilter2';
	var blurSize1= 3;
	var shadowXOffset1= 2;
	var shadowYOffset1= 2;
	var blurSize2= 4;
	var shadowXOffset2= 3;
	var shadowYOffset2= 3;
	//confidence legend
	var displayConfidenceLevelLegend= true;
	var confidenceLevelLegendFontSize= 12;
	//old color map values [245, 24, 54], [245, 113, 113], [247, 223, 114], [129, 247, 114], [58, 252, 33]
	var confidenceLevelLegendColorMap= [[200, 248, 190], [169, 248, 153], [123, 234, 100], [115, 182, 101], [60, 161, 39]];
	var confidenceLevelLegendXOffset= 10; //offset from the chart (to the left)
	var confidenceLevelLegendLabelXOffset= 5; //offset from the label to the color indicator
	var confidenceLevelLegendColorIndicatorXOffset= 5; //offset from the most left element to the color indicator
	var confidenceLevelLegendColorIndicatorYOffset= 5; //offset from the most to element to the color indicator
	var confidenceLevelLegendColorIndicatorWidth= 15;
	var confidenceLevelLegendLabelToBorder= 5; //offset from the biggest label to the boarder of the legend
	var confidenceLevelLegendLabelColor= [70, 128, 235];
	var confidenceLevelLegendLabelFontName= 'Ariel';
	var confidenceLevelLegendBorderColor= [199, 199, 199];
	var confidenceLevelLegendLineThickness= 2;
	var confidenceLevelLegendBackgroundColor= [255, 255, 255];
	/* End settings */
	
	var ratingSvgTextNodes= [];
	var confidenceLevelSvgTextNodes= [];
	var cellWidth= minCellWidth;
	var cellHeight= minCellHeight;
	var cellGroupWidth= 0;
	var cellGroupHeight= 0;
	var cellGroupTotalXOffset= 0;
	var cellGroupTotalYOffset= 0;
	var confidenceLevelTextNode= null;
	var confidenceLevelLabelsMaxWidth= 0;
	var confidenceLevelLabelsTotalXOffset= 0; //total x offset from the left of the start point of the document
	var confidenceLevelLabelsTotalYOffset= 0; //total y offset of the confidence level label that should be place in the bottom of the chart (the first label)
	var confidenceLevelLabelTotalYOffset= 0;
	var rulerXStartPoint= 0;
	var rulerYStartPoint= 0;
	var confidenceLevelLegendLabelSvgTextNodes= [];
	var confidenceLevelLegendInsideWidth= 0;
	var confidenceLevelLegendInsideHeight= 0;
	var confidenceLevelLegendLabelMaxWidth= 0;
	
	//var ratingLabelsGroup= svg.group(null, 'ratingLabelsGroup', null);
	//var confidenceLevelLabelsGroup= svg.group(null, 'confidenceLevelLabelsGroup', null);
	var globalDef= svg.defs(null, 'globalDef', null);
	var rulerGroup= svg.group(null, 'rulerGroup', {filter: createFilterLink(shadowFilterId1)});
	var rulerArrowGroup= svg.group(rulerGroup, 'rulerArrowGroup', {filter: createFilterLink(shadowFilterId1)});
	var cellGroup= svg.group(null, 'cellGroup', {filter: createFilterLink(shadowFilterId2)});
	var rulerMarkerGroup= svg.group(null, 'rulerMarkersGroup', {filter: createFilterLink(shadowFilterId1)});
	var rulerMarkerLabelGroup= svg.group(rulerMarkerGroup, 'rulerMakerLabelGroup', null);
	var rulerMarkerLabelConfidenceLevelGroup= svg.group(rulerMarkerLabelGroup, 'rulerMarkerLabelConfidenceLevelGroup', null);
	var rulerMarkerLabelRatingGroup= svg.group(rulerMarkerLabelGroup, 'rulerMarkerLabelRatingGroup', null);
	var confidenceLevelLegendGroup= svg.group(null, 'confidenceLevelLegendGroup', null);
	var confidenceLevelLegendBodyGroup= svg.group(confidenceLevelLegendGroup, 'confidenceLevelLegendBodyGroup', null);
	var confidenceLevelLegendColorIndicatorGroup= svg.group(confidenceLevelLegendGroup, 'confidenceLevelLegendColorIndicatorGroup', null);
	var confidenceLevelLegendLabelsGroup= svg.group(confidenceLevelLegendGroup, 'confidenceLevelLegendLabelsGroup', null);
	
	//because we need to know the width of the text to place the some of the items, create all the labels before anything else
	
	//rating labels
	for(i= 0; i < ratings.length; i++)
	{
		temp= null;
		ratingSvgTextNodes[i]= svg.text(rulerMarkerLabelRatingGroup, null, null, ratings[i], {fontSize: fontSize + 'px', fontFamily: rulerFontName, fill: createRgbString(rulerFontColor)});
		temp= ratingSvgTextNodes[i].getComputedTextLength();
		//check if the label is not too big, if it is remove some letters
		if (temp > rulerLabelRatingMaxWidth)
		{
			var node= ratingSvgTextNodes[i];
			var nChars= node.getNumberOfChars();
			node.firstChild.insertData(nChars, '...');
			for(var j= 1; temp > rulerLabelRatingMaxWidth && j != nChars; j++)
			{
				node.firstChild.deleteData(nChars - j, 1);
				temp= node.getComputedTextLength();
			}
		}
		if ( temp > cellWidth)
		{
			cellWidth= temp;
		}
	}
	
	//the height of the cell is based on the height of the confidential level label but the size is fixed so there is no need to calculate it
	
	//create the confidence level labels, confidence level legend labels and calculate the max width of the label
	for(i= 0; i < confidenceLevels.length; i++)
	{
		temp= null;
		confidenceLevelSvgTextNodes[i]= svg.text(rulerMarkerLabelConfidenceLevelGroup, null, null, confidenceLevels[i], {fontSize: fontSize + 'px', fontFamily: rulerFontName, fill: createRgbString(rulerFontColor)});
		temp= confidenceLevelSvgTextNodes[i].getComputedTextLength();
		//check if the label is not too big, if it is remove some letters
		if (temp > rulerLabelConfidenceLevelMaxWidth)
		{
			var node= confidenceLevelSvgTextNodes[i];
			var nChars= node.getNumberOfChars();
			node.firstChild.insertData(nChars, '...');
			for(var j= 1; temp > rulerLabelConfidenceLevelMaxWidth && j != nChars; j++)
			{
				node.firstChild.deleteData(nChars - j, 1);
				temp= node.getComputedTextLength();
			}
		}
		if( temp > confidenceLevelLabelsMaxWidth)
		{
			confidenceLevelLabelsMaxWidth= temp;
		}
		if(displayConfidenceLevelLegend == true)
		{
			confidenceLevelLegendLabelSvgTextNodes[i]= svg.text(confidenceLevelLegendLabelsGroup, null, null, confidenceLevelSvgTextNodes[i].firstChild.data, {fontSize: confidenceLevelLegendFontSize + 'px', fontFamily: confidenceLevelLegendLabelFontName, fill: createRgbString(confidenceLevelLegendLabelColor)})
			temp= confidenceLevelLegendLabelSvgTextNodes[i].getComputedTextLength();
			if( temp > confidenceLevelLegendLabelMaxWidth)
			{
				confidenceLevelLegendLabelMaxWidth= temp;
			}
		}
	}
	
	//create the axis labels
	confidenceLevelTextNode= svg.text(null, null, null, confidenceLevelWord, {fontSize: confidenceLevelFontSize + 'px', fontFamily: axisFontName, fill: createRgbString(axisFontColor), filter: createFilterLink(shadowFilterId1)});
	ratingTextNode= svg.text(null, null, null, ratingWord, {fontSize: ratingFontSize + 'px', fontFamily: axisFontName, fill: createRgbString(axisFontColor), filter: createFilterLink(shadowFilterId1)});
	
	/* pre calculations */
	
	//calculate the final cell height and width
	cellWidth+= cellExtraHeight * 2;
	if(cellHeight < fontSize)
	{
		cellHeight= fontSize;
	}
	cellHeight+= cellExtraHeight * 2;
	
	if(cellHeight > cellWidth)
	{
		cellWidth= cellHeight;
	}
	else if(cellWidth > cellHeight)
	{
		cellHeight= cellWidth;
	}
	
	//calculate the size of the total cell group
	
	cellGroupWidth= cellWidth * ratings.length + (cellLineThickness * (ratings.length * 2));
	cellGroupHeight= cellHeight * confidenceLevels.length + (cellLineThickness * (confidenceLevels.length * 2));
	
	cellGroupTotalYOffset= chartYOffset + arrowHeight + rulerExtraHeight + cellGroupHeight;
	
	//check if the confidence level label and the rating label sizes will fit the chart
	{
		//confidence level
		var confidenceLevelWidth= confidenceLevelTextNode.getComputedTextLength();
		//in case the label is bigger then the chart it self, reduce the size of the label
		if(confidenceLevelWidth > cellGroupHeight)
		{
			for(i= 0; confidenceLevelWidth > cellGroupHeight; i++)
			{
				$(confidenceLevelTextNode).attr('font-size', confidenceLevelFontSize - i);
				confidenceLevelWidth= confidenceLevelTextNode.getComputedTextLength();
			}
			confidenceLevelFontSize-= i;
		}
		
		//ranting
		var wordLength= ratingTextNode.getComputedTextLength();
		if(wordLength > cellGroupWidth)
		{
			for(i= 0; wordLength > cellGroupWidth; i++)
			{
				$(ratingTextNode).attr('font-size', ratingFontSize - i);
				wordLength= ratingTextNode.getComputedTextLength();
			}
			ratingFontSize-= i;
		}
	}
	
	//calculate the total y offset of the confidence level label
	confidenceLevelLabelTotalYOffset= chartYOffset + arrowHeight + rulerExtraHeight
	
	//calculate the x offset of the confidence level labels, the confidence level label is set to be display in the vertical, so the true width is the height
	confidenceLevelLabelsTotalXOffset= confidenceLevelLabelXOffset + confidenceLevelFontSize + confidenceLevelLabelsXOffset;
	confidenceLevelLabelsTotalYOffset= chartYOffset + arrowHeight + rulerExtraHeight + cellGroupHeight + (rulerLineThickness / 2);
	
	//calculate the start of the ruler
	rulerXStartPoint= confidenceLevelLabelsTotalXOffset + confidenceLevelLabelsMaxWidth + rulerMarkerToLabelYOffset + rulerMarkerHeight / 2;
	rulerYStartPoint= chartYOffset + arrowHeight + rulerExtraHeight + cellGroupHeight + rulerLineThickness / 2;
	
	//calculate the inside height and width of the confidence level legend
	confidenceLevelLegendInsideWidth= confidenceLevelLegendColorIndicatorXOffset + confidenceLevelLegendColorIndicatorWidth + confidenceLevelLegendLabelXOffset + confidenceLevelLabelsMaxWidth + confidenceLevelLegendLabelToBorder;
	confidenceLevelLegendInsideHeight= confidenceLevelLegendColorIndicatorYOffset * (confidenceLevels.length + 1) + confidenceLevelLegendFontSize * confidenceLevels.length;  
	
	/* End pre calculation */
	
	/* Set the size of the svg*/
	{
		// +20 to give extra space for the shadow
		var width= rulerXStartPoint + cellGroupWidth + rulerExtraHeight + arrowHeight + 20;
		var height= rulerYStartPoint + rulerMarkerHeight /2 + rulerMarkerToLabelYOffset + fontSize + ratingLabelYOffset + ratingFontSize + 20;
		
		if(displayConfidenceLevelLegend == true)
		{
			width+= confidenceLevelLegendXOffset + confidenceLevelLegendInsideWidth;
			// the confidence level legend is placed next to the chart aligned to the top of the chart minus arrow and extra ruler height, this means not all the time it will be heighter than the chart
			var temp= rulerYStartPoint - chartYOffset - arrowHeight - rulerExtraHeight;
			temp+= rulerMarkerHeight / 2 + rulerMarkerToLabelYOffset + fontSize + ratingLabelYOffset + ratingFontSize;
			if(temp < confidenceLevelLegendInsideHeight)
			{
				height+= confidenceLevelLegendInsideHeight - temp;
			}
		}
		svg.configure({width: width + 'px', height: height + 'px', viewbox: '0 0 ' + width + ' ' + height, preserveAspectRatio: 'xMidYMid meet'});
	}
	/* End set the size of the svg*/
	
	/* Place the confidence level label */
	
	//rotate the the label as the write mode attribute doesn't work with firefox
	{
		var x= confidenceLevelLabelXOffset;
		var y= confidenceLevelLabelTotalYOffset + cellGroupHeight / 2 + confidenceLevelFontSize / 2;
		$(confidenceLevelTextNode).attr('x', x);
		$(confidenceLevelTextNode).attr('y', y);
		$(confidenceLevelTextNode).attr('transform', 'rotate(90 ' + x + ' ' + y + ') ' + 'translate( ' + (-( (confidenceLevelTextNode.getComputedTextLength() / 2) + (rulerLineThickness / 2) )) +' )');
	}
	/* End create and place the confidence level label */
	
	/* Create and place the rating label */
	
	$(ratingTextNode).attr('x', rulerXStartPoint + cellGroupWidth / 2 - (ratingTextNode.getComputedTextLength() / 2));
	$(ratingTextNode).attr('y', rulerYStartPoint + rulerMarkerHeight / 2 + rulerMarkerToLabelYOffset + fontSize + ratingFontSize + ratingLabelYOffset);
	
	/* End create and place the rating label */
	
	/* Place the confidence levels labels */
	//use of brackets to make sure the variables used are removed after they are used
	{
		var x= confidenceLevelLabelsTotalXOffset;
		var y= 0;
		for(var i= 0; i < confidenceLevelSvgTextNodes.length; i++)
		{
			//the placement of the first label is in the bottom.
			y= confidenceLevelLabelsTotalYOffset - (rulerLineThickness / 2) - cellLineThickness - (cellHeight/2) - (i * cellHeight) - ((i * cellLineThickness) * 2) + (confidenceLevelFontSize / 2);
			$(confidenceLevelSvgTextNodes[i]).attr('x', x);
			$(confidenceLevelSvgTextNodes[i]).attr('y',  y);
		}
	}
	
	/* Place the rating labels */
	//use of brackets to make sure the variables used are removed after they are used
	{
		var tempPoint1= rulerXStartPoint + cellLineThickness + cellWidth / 2;
		var tempPoint2= rulerYStartPoint + rulerMarkerHeight / 2 + rulerMarkerToLabelYOffset + fontSize;
		var x= 0;
		var y= 0;
		for(var i= 0; i < ratings.length; i++)
		{
			x= tempPoint1 - ratingSvgTextNodes[i].getComputedTextLength() / 2 + (i * cellWidth) + ((i * cellLineThickness) * 2);
			y= tempPoint2
			$(ratingSvgTextNodes[i]).attr('x', x);
			$(ratingSvgTextNodes[i]).attr('y', y);
		}
	}
	/* End place the rating labels */
	
	/* End place the confidence levels labels */
	
	/* Create and place the ruler */
	//use the brackets so the variables are not visible from outside
	{
		var x1= confidenceLevelLabelsTotalXOffset + confidenceLevelLabelsMaxWidth + rulerMarkerToLabelYOffset + rulerMarkerHeight/2;
		var y1= chartYOffset + arrowHeight;
		var x2= x1;
		var y2= y1 + cellGroupHeight + rulerExtraHeight + rulerLineThickness / 2;
		var x3= x2 + cellGroupWidth + rulerExtraHeight + rulerLineThickness / 2;
		var y3= y2;
		svg.polyline(rulerGroup, [[x1, y1], [x2, y2], [x3, y3]], {strokeWidth: rulerLineThickness, fill: 'none', stroke: createRgbString(rulerColor)});
	}
	/* End create and place the ruler */
	
	/* Create and place the ruler markers */
	//brackets are used to make sure the variables are destroyed after it is needed
	{
		var tempPoint= rulerYStartPoint;
		var x1= 0;
		var y1= 0;
		var x2= 0;
		var y2= 0;
		//confidence level
		for(var i= 0; i < confidenceLevels.length; i++)
		{
			x1= confidenceLevelLabelsTotalXOffset + confidenceLevelLabelsMaxWidth + rulerMarkerToLabelYOffset;
			y1= tempPoint - cellLineThickness - (cellHeight / 2) - ((cellHeight * i) + ((i * cellLineThickness) * 2));
			x2= x1 + rulerMarkerHeight;
			y2= y1;
			svg.line(rulerMarkerGroup, x1, y1, x2, y2, {strokeWidth: rulerMarkerLineWidth, stroke: createRgbString(rulerMarkerColor)});
		}
		
		//rating
		tempPoint= rulerXStartPoint + cellLineThickness + cellWidth / 2;
		var tempPoint2= rulerYStartPoint + rulerMarkerHeight / 2;
		for(var i= 0; i < ratings.length; i++)
		{	
			x1= tempPoint + (cellWidth * i) + ((i * cellLineThickness) * 2);
			y1= tempPoint2;
			x2= x1;
			y2= y1 - rulerMarkerHeight;
			svg.line(rulerMarkerGroup, x1, y1, x2, y2, {strokeWidth: rulerMarkerLineWidth, stroke: createRgbString(rulerMarkerColor)});
		}
	}
	
	/* End create and place the ruler markers */
	
	/* Create and place the arrows in the ruler */
	{
		var x1= 0;
		var y1= 0;
		var x2= 0;
		var y2= 0;
		var x3= 0;
		var y3= 0;
		
		//top arrow
		x1= rulerXStartPoint - arrowWidth / 2;
		y1= chartYOffset + arrowHeight;
		x2= x1 + arrowWidth / 2;
		y2= y1 - arrowHeight;
		x3= x2 + arrowWidth / 2;
		y3= y2 + arrowHeight;
		svg.polyline(rulerArrowGroup, [[x1, y1], [x2, y2], [x3, y3]], {stroke: 'none', fill: createRgbString(arrowColor)});
		
		//bottom arrow
		x1= rulerXStartPoint + cellGroupHeight + rulerExtraHeight;
		y1= rulerYStartPoint - arrowHeight / 2;
		x2= x1;
		y2= y1 + arrowHeight;
		x3= x2 + arrowWidth;
		y3= y2 - arrowHeight / 2;
		svg.polyline(rulerArrowGroup, [[x1, y1], [x2, y2], [x3, y3]], {stroke: 'none', fill: createRgbString(arrowColor)});
	}
	
	/* End create and place the arrows in the ruler */
	
	/* Create the cells */
	{
		var x= 0;
		var y= 0;
		var tempX= rulerXStartPoint + cellLineThickness / 2;
		var tempY= rulerYStartPoint - cellLineThickness - cellHeight - cellLineThickness /2;
		var temp= null;
		var cellRowGroup= null;
		for(var i= 0; i < confidenceLevels.length; i++)
		{
			cellRowGroup= svg.group(cellGroup, 'cellRowGroup' + i, null);
			y= tempY - (i * cellHeight) - ((i * cellLineThickness) * 2);
			for(var j= 0; j < ratings.length; j++)
			{
				x= tempX + (j * cellWidth) + ((j * cellLineThickness) * 2);
				temp= svg.rect(cellRowGroup, x, y, cellWidth, cellHeight, {strokeWidth: cellLineThickness, stroke: 'none', fill: createRgbString(cellColor), opacity: 0.7, style: 'cursor: ' + cellCursor + ';'});
				//append custom attribute, this is compatible with html5
				$(temp).attr('data-colvalue', j);
				$(temp).attr('data-rowvalue', i);
				$(temp).mouseover(highlightBackground);
				$(temp).mouseout(cellColor, removeHighlightFromBackground);
				$(temp).mousedown(highlightMouseDown);
				$(temp).mouseup(removeHighlightMouseDown)
				if(returnFunction != null)
				{
					$(temp).click({returnFunction: returnFunction, ratings: ratings, confidenceLevels: confidenceLevels}, onClickHandler);
				}
			}
		}
	}	
	/* End create the cells*/
	
	/* Create shadowFilter */
	{
		var filter= svg.filter(globalDef, shadowFilterId1, null, null, '150%', '150%');
		svg.filters.offset(filter, 'offOut', 'SourceGraphic', shadowXOffset1, shadowYOffset1);
		svg.filters.gaussianBlur(filter, 'blurOut', 'offOut', blurSize1);
		svg.filters.blend(filter, null, 'normal', 'SourceGraphic', 'blurOut');
		
		filter= svg.filter(globalDef, shadowFilterId2, null, null, '150%', '150%');
		svg.filters.offset(filter, 'offOut', 'SourceGraphic', shadowXOffset2, shadowYOffset2);
		svg.filters.gaussianBlur(filter, 'blurOut', 'offOut', blurSize2);
		svg.filters.blend(filter, null, 'normal', 'SourceGraphic', 'blurOut');
	}
	/* End create shadow filer*/
	
	/* create the confidence level chart*/
	{
		if(displayConfidenceLevelLegend == true)
		{
			// create the main body of the legend
			var xLegendStartPoint= rulerXStartPoint + cellGroupWidth + rulerExtraHeight + arrowHeight + confidenceLevelLegendXOffset;
			var yLegendStartPoint= rulerYStartPoint - cellGroupHeight;
			svg.rect(confidenceLevelLegendBodyGroup, xLegendStartPoint, yLegendStartPoint, confidenceLevelLegendInsideWidth + 'px', confidenceLevelLegendInsideHeight + 'px', {strokeWidth: confidenceLevelLegendLineThickness, fill: createRgbString(confidenceLevelLegendBackgroundColor), stroke: createRgbString(confidenceLevelLegendBorderColor), filter: createFilterLink(shadowFilterId1), rx: 5, ry: 5});
			
			// create the color legends with labels
			var yBase= yLegendStartPoint + confidenceLevelLegendColorIndicatorYOffset;
			var xColorIndicator= xLegendStartPoint + confidenceLevelLegendColorIndicatorXOffset;
			var y= 0;
			var xLabel= xColorIndicator + confidenceLevelLegendColorIndicatorWidth + confidenceLevelLegendColorIndicatorXOffset;
			for(var i= 0; i < confidenceLevels.length; i++)
			{
				//height of the color indicator is the same as the font height of the legend
				//color indicatoryColorIndicator
				y= yBase + i * confidenceLevelLegendFontSize  + i * confidenceLevelLegendColorIndicatorYOffset;
				svg.rect(confidenceLevelLegendColorIndicatorGroup, xColorIndicator, y, confidenceLevelLegendColorIndicatorWidth + 'px', confidenceLevelLegendFontSize + 'px', {fill: createRgbString(confidenceLevelLegendColorMap[i]), strokeWidth: 0, rx: 2, ry: 2}); 
				//labels
				// - 2 to put the label in the correct place
				y+= confidenceLevelLegendFontSize - 2;
				svg.configure(confidenceLevelLegendLabelSvgTextNodes[i], {x: xLabel, y: y});
			}
		}
	}
}

function createRgbString(code)
{
	return 'rgb(' + code[0] + ',' + code[1] + ',' + code[2] + ')'; 
}

/**
 * This function will return a string that is used to link an element to a filter
 * @param filterId filter id
 */
function createFilterLink(filterId)
{
	return 'url(#' + filterId + ')';
}
/**
 * This function will highlight the col and row backgroud of the cells of the chart 
 * @param event mouse event
 */
function highlightBackground(event)
{
	var fillColorNotSelected= [184, 245, 217];
	var fillColorSelected= [159, 227, 180];
	var target= $(event.target);
	var rowGroup= target.parent('g');
	var rowGroupCells= rowGroup.children();
	var colSelected= parseInt(target.attr('data-colvalue'));
	var rowSelected= parseInt(target.attr('data-rowvalue'));
	var rows= target.parents('#cellGroup').children();
	var temp= null;
	
	//row
	for(var i= 0; i < colSelected; i++)
	{
		$(rowGroupCells[i]).attr('fill', createRgbString(fillColorNotSelected));
	}
	
	//cols
	for(var i= 0; i < rowSelected; i++)
	{
		temp= $(rows[i]).children();
		$(temp[colSelected]).attr('fill', createRgbString(fillColorNotSelected));
	}
	target.attr('fill', createRgbString(fillColorSelected));
}

/**
 * This function will remove the background highlight of the cells of the chart
 * @param event mouse event
 */
function removeHighlightFromBackground(event)
{
	var target= $(event.target);
	var rowGroup= target.parent('g');
	var rowGroupCells= rowGroup.children();
	var colSelected= parseInt(target.attr('data-colvalue'));
	var rowSelected= parseInt(target.attr('data-rowvalue'));
	var rows= target.parents('#cellGroup').children();
	var temp= null;
	
	//rows
	for(var i= 0; i < colSelected; i++)
	{
		$(rowGroupCells[i]).attr('fill', createRgbString(event.data));
	}
	
	//cols
	for(var i= 0; i < rowSelected; i++)
	{
		temp= $(rows[i]).children();
		$(temp[colSelected]).attr('fill', createRgbString(event.data));
	}
	target.attr('fill', createRgbString(event.data));
}

/**
 * The function will change the color of the rect when the mouse is pressed down
 * @param event mouse event
 */
function highlightMouseDown(event)
{
	var colorHighlight= [56, 166, 89];
	$(event.target).attr('fill', createRgbString(colorHighlight));
}

/**
 * This function will change the cell background back to normal when the mouse button is released
 * @param event mouse event
 */
function removeHighlightMouseDown(event)
{
	var colorHighlight= [159, 227, 180];
	$(event.target).attr('fill', createRgbString(colorHighlight));
}

/**
 * This function will handle when the user click on the cell of the chart
 * @param event mouse event
 */
function onClickHandler(event)
{
	var returnFunction= event.data.returnFunction;
	var rowN= parseInt($(event.target).attr('data-rowvalue'));
	var colN= parseInt($(event.target).attr('data-colvalue'));
	var ratingName= event.data.ratings[colN];
	var confidenceName= event.data.confidenceLevels[rowN];
	returnFunction(rowN, colN, ratingName, confidenceName);
}
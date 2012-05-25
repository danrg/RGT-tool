var urlStaticFiles= '/static/';
//load other javascript needed for the showMyGrids.html
if(!jQuery.svg)
{
	$.ajax({
		url: urlStaticFiles + 'js/svg/jquery.svg.js',
		dataType: 'script',
		async:   false 
	});
	
	$.ajax({
		url: urlStaticFiles + 'js/svg/jquery.svgfilter.js',
		dataType: 'script',
		async:   false 
	});
}

function clearSvgImg(divId)
{
	$('#' + divId).svg('destroy');
}

/**
 * 
 * @param divTag jquery object representing the div where the svg is located
 */
function getSvgFromDiv(divTag)
{
	return divTag.svg('get');
}

function createDendogram(divId, xmlData)
{
	$('#' + divId).svg();
	var svg= $('#' + divId).svg('get');
	var properties= new Properties($(xmlData).find('properties'));
	
	svg.configure({viewBox: '0 0 ' + properties.getWidth() + ' ' + properties.getHeight(), width: properties.getWidth(), height: properties.getHeight()}, true);
	createShadowFilter(svg, null, properties.getShadow());
	var groupMain= svg.group(null, 'mainGroup', {filter: 'url(#shadowFilter)'});
	
	
	//draw the table
	$(xmlData).find('dendogramTable').each(function(){
		//draw all the lines first
		$(this).find('line').each(function(){
				drawLine(svg, groupMain, $(this));
		});
		
		//draw all the text
		$(this).find('text').each(function(){
			drawText(svg, groupMain, $(this));
		});
	});
	
	//now lets draw the concern dendogram
	$(xmlData).find('dendogramConcerns').each(function(){
		//draw all the lines first
		$(this).find('line').each(function(){
				drawLine(svg, groupMain, $(this));
		});
		
		//draw all the text
		$(this).find('text').each(function(){
			drawText(svg, groupMain, $(this));
		});	
	});
	
	//now lets draw the alternative dendogram
	$(xmlData).find('dendogramAlternative').each(function(){
		//draw all the lines first
		$(this).find('line').each(function(){
				drawLine(svg, groupMain, $(this));
		});
		
		//draw all the text
		$(this).find('text').each(function(){
			drawText(svg, groupMain, $(this));
		});	
	});
}

function drawLine(svg, parent, xmlLineNode)
{
	var startX, startY, endX, endY, width;
	var color;
	startX= parseInt(xmlLineNode.find('startX').text());
	startY= parseInt(xmlLineNode.find('startY').text());
	endX= parseInt(xmlLineNode.find('endX').text());
	endY= parseInt(xmlLineNode.find('endY').text());
	width= parseInt(xmlLineNode.find('width').text());
	color= getColor(xmlLineNode.find('color'));
	
	svg.line(parent, startX, startY, endX, endY, {stroke: 'rgb('+ color[0] + ',' + color[1] + ',' + color[2] + ')', 'stroke-width': width });

}

function drawText(svg, parent, xmlTextNode)
{
	var x, y, height, textValue;
	
	x= parseInt(xmlTextNode.find('x').text());
	y= parseInt(xmlTextNode.find('y').text());
	height= parseInt(xmlTextNode.find('height').text());
	textValue= xmlTextNode.find('textValue').text()
	fontData= getFontData(xmlTextNode.find('font'));
	svg.text(parent, x, y + height - 5, textValue, {'font-family': fontData['name'], fill: 'rgb(' + color[0] + ',' + color[1] + ',' + color[2] + ')', 'font-size': fontData['size']});
}

function getFontData(fontNode)
{
	var map= {};
	var fontName, fontSize;
	var fillColor;
	
	fontName= fontNode.find('name').text();
	fontSize= parseInt(fontNode.find('size').text());
	fillColor= getColor(fontNode.find('fill>color'));
	
	map['name']= fontName;
	map['size']= fontSize;
	map['fillColor']= fillColor;
	return map;
}

function getColor(colorNode)
{
	color= new Array(4);
	color[0]= parseInt(colorNode.find('red').text())
	color[1]= parseInt(colorNode.find('green').text())
	color[2]= parseInt(colorNode.find('blue').text())
	color[3]= parseInt(colorNode.find('alpha').text())
	return color;
}

/**
 * 
 * @param svg svg element 
 * @param parent the parent of the shadow filter, if null, the svg root will be use
 * @param shadowData an instance of the Shadow class
 * @returns
 */
function createShadowFilter(svg, parent, shadowData)
{
	var filter= svg.filter(parent, 'shadowFilter', null, null, '150%', '150%');
	svg.filters.offset(filter, 'offOut', 'SourceGraphic', shadowData.getXOffSet(), shadowData.getYOffSet());
	svg.filters.gaussianBlur(filter, 'blurOut', 'offOut', shadowData.getBlurSize());
	svg.filters.blend(filter, null, 'normal', 'SourceGraphic', 'blurOut');
	return filter;
}

//class properties
function Properties(xmlPropertyNode)
{
	//private global variables
	var width= null;
	var height= null;
	var shadow= null;
	var useGlobalShadow= false;
	
	//public global variables
	this.SHADOW_PROPERTY_XOFFSET= 'xOffSet';
	this.SHADOW_PROPERTY_YOFFSET= 'yOffSet';
	this.SHADOW_PROPERTY_BLURSIZE= 'blurSize';
	
	//constructor
	{
		width= parseInt(xmlPropertyNode.find('width').text());
		height= parseInt(xmlPropertyNode.find('height').text());
		
		//check if we want global shadows
		var shadowNode= xmlPropertyNode.find('shadow');
		if(shadowNode.length >= 1)
		{
			useGlobalShadow= true;
			//get the shadow obj
			shadow= new Shadow(shadowNode);
		}
	}
	
	
	this.getWidth= function()
	{
		return width;
	}
	
	this.getHeight= function()
	{
		return height;
	}
	
	this.useGlobalShadow= function()
	{
		return useGlobalShadow;
	}
	
	this.getShadow= function()
	{
		return shadow;
	}
	
	this.getShadowProperty= function(property)
	{
		if(useGlobalShadow)
		{
			switch(property)
			{
				case this.SHADOW_PROPERTY_XOFFSET:
				{
					return shadow.getXOffSet();
				}
				case this.SHADOW_PROPERTY_YOFFSET:
				{
					return shadow.getYOffSet();
				}
				case this.SHADOW_PROPERTY_BLURSIZE:
				{
					return shadow.getBlurSize();
				}
				default:
				{
					return null;
				}
			}
		}
		return null;
	}
}

//class shadow
function Shadow(shadowNode)
{

	//private global variables
	var xOffSet= null;
	var yOffSet= null;
	var blurSize= null;
	
	//constructor
	{
		xOffSet= parseInt(shadowNode.find('xOffSet').text());
		yOffSet= parseInt(shadowNode.find('yOffSet').text());
		blurSize= parseInt(shadowNode.find('blurSize').text());
	}
	
	this.getXOffSet= function()
	{
		return xOffSet;
	}

	this.getYOffSet= function()
	{
		return yOffSet;
	}
	
	this.getBlurSize= function()
	{
		return blurSize;
	}
}
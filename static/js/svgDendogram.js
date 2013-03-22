var urlStaticFiles = '/static/';

/**
 * Remove the svg element
 * @param divId the div id that contains the svg element
 */
function clearSvgImg(divId)
{
	$('#' + divId).find('svg').remove();
}

/**
 * 
 * @param divTag jquery object representing the div where the svg is located
 */
function getSvgFromDiv(divTag)
{
	return divTag.find('svg');
}

/**
 * Function used to convert a svg xml doc into a string
 * @param svgElement Jquery object containing the svg element
 */
function getSvgString(svgElement)
{
	var serializer = new XMLSerializer();
	return serializer.serializeToString(svgElement[0]);
}

/**
 * This function will create/add the svg image to the div
 * @param divId String with the div id
 * @param xmlData String xml document
 */
function createDendogram(divId, xmlData)
{
	//import contents of the svg document into this document
	var importedSVGRootElement = document.importNode(xmlData.documentElement, true);
	//append the imported SVG root element to the appropriate HTML element
	$('#' + divId).append(importedSVGRootElement);
}


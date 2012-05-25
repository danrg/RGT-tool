function showLoadingSpinner(element, msg)
{
	if( msg == null)
	{
		element.mask("Loading...");
	}
	else
	{
		element.mask(msg);
	}
}

function hideLoadingSpinner(element)
{
	element.unmask();
}
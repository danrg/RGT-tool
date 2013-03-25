function addConcern(conObj, imgObj)
{
    var column = $(imgObj + "[onclick^='addRow']:first");
    column.click();
    var concernsLeft = $(conObj).find('td:first-child');
    var conLeftHtml = $(concernsLeft).html();
    var concernsRight = $(concernsLeft).next();
    var conRightHtml = $(concernsRight).html();
    var inputConLeft = $("input[id*='left']:last");
    var inputConRight = $("input[id*='right']:last");
    inputConLeft.val(conLeftHtml);
    inputConRight.val(conRightHtml);
}

function addAlt(altObj, imgObj)
{
    var firstRow = $(imgObj + "[onclick^='addCol']:first");
    firstRow.click();
    var alternatives = $(altObj).find('td:first-child');
    var altHtml = $(alternatives).html();
    var inputAlt = $("input[id^='alternative']:last");
    inputAlt.val(altHtml);
}

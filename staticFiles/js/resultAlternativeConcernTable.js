//$.ajax({
//		url: 'https://www.google.com/jsapi',
//		dataType: 'script',
//		async:   false 
//	});

//if(!jQuery.getRowAndCellIndex)
//{
//	$.ajax({
//		url: urlStaticFiles + 'js/RowAndCellIndex.js',
//		dataType: 'script',
//		async:   false 
//	});
//}

//function getCharts()
//{
//	//google.load("visualization", "1", {packages:["corechart"]});
//	google.setOnLoadCallback(showCharts);
//	 
//	
//}

function showCharts()
{
	alert('la');
//	console.log('drawing charts');
//	 var data = google.visualization.arrayToDataTable([['Year', 'Sales', 'Expenses'], ['2004', 1000, 400]]);
//	 
//	 
//	 var chart = new google.visualization.ColumnChart(document.getElementById('concenrsChartDiv'));        
//	 chart.draw(data, null);
}

/**
 * this function will convert a 2 by N table into an array. The first col should contain the names, the first cell of each row should contain the category name
 * @param tableObj Jquery object representing the table
 */
//function getTableData(tableTag)
//{
//	var matrix= [['Concerns', '']];
//	var tempArray= null;
//	var tBody= tableTag.find('tbody');
//	
//	
//	tBody.find('tr').each(function(){
//		
//		tempArray= [];
//		$(this).find('td').each(function(){
//			tempArray.push($(this).text());
//		});
//		
//		matrix.push(tempArray);
//	});
//	console.log(matrix);
//}
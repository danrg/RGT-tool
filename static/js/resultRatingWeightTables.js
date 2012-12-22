var resultIndividualRatioChart= null;

/**
 * 
 * @param data is a matrix, format: [['name',value], .....]
 */
function displayChartOfRatings(data)
{
	var chartData= [];
	var chartOptions= null;
	// create the data for the chart
	for (var i= 0; i < data.length; i++)
	{
		chartData.push({name: data[i][0], data: [data[i][1]]});
	}
	chartOptions= {
			chart: {
				renderTo: 'chartDisplay',
				type: 'column'
			},	
			title:{
				text: 'Grid Ratios'
			},
			xAxis: {
	            categories: ['Proposed ratio']
	         },
	         yAxis: {
	             title: {
	                text: 'Ratio'
	             }
	         },
			series: chartData
		};
	if(resultIndividualRatioChart == null)
	{
		
		resultIndividualRatioChart= new Highcharts.Chart(chartOptions);
	}
	else
	{
		resultIndividualRatioChart.destroy();
		resultIndividualRatioChart= new Highcharts.Chart(chartOptions);
	}
}

/**
 * Remove all the chart that are created by this script
 */
function clearRatioResultCharts()
{
	if(resultIndividualRatioChart != null)
	{
		resultIndividualRatioChart.destroy();
		resultIndividualRatioChart= null;
	}
}
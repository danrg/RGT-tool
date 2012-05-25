/**
 * @returns Array, first position contains the row index and the second position contains the colIndex
 */
$(document).ready(function(){
	$.fn.getRowAndCellIndex = function() { 
		    	if(! $(this).is('td') && ! $(this).is('th')){
		        	return -1; 
		    	}
		 
		    	var row= this.parent('tr');
		    	var tbody= row.parent('tbody');
		    	var rowIndex= tbody.children().index(row);
		   		var allCells = row.children(); 
		   		var normalIndex = allCells.index(this); 
		    	var nonColSpanIndex = 0; 
		 
			    allCells.each( 
			        function(i, item) 
			        { 
			            if(i == normalIndex) 
			                return false; 
			 
			            var colspan = $(this).attr('colspan'); 
			            colspan = colspan ? parseInt(colspan) : 1; 
			            nonColSpanIndex += colspan; 
			        } 
			    ); 
	    		return [rowIndex, nonColSpanIndex];
			}
});
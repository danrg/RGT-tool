$(document).ready(function () {
	$('#btn-add').click(function () {
        var i = 1;
        var finished = false;
        var fieldStr = "#alt-list-data-";
        var alternateStr = "#alternate_grid-";
        while(!finished)
        {
            var dummyStr = "";
            dummyStr = fieldStr + i.toString();
            if($(dummyStr).length)
            {
                i++;
            }
            else
            {
                finished = true;
            }
        }

        var numFields = i-1;
        var rule = "";
        for(var j=1; j<=numFields; j++)
        {
            var oneChecked = false;
            var finishedAlternates = false;
            var firstRule = true;
            var dummyStr = "";
            var k = 1;
            dummyStr = fieldStr + j.toString();
            while(!finishedAlternates)
            {
                var dummyStr2 = "";
                dummyStr2 = alternateStr + j.toString() + '-' + k.toString();

                if($(dummyStr2).length)
                {
                    k++;

                    if($(dummyStr2).is(':checked'))
                    {
                        oneChecked = true;
                        if(firstRule)
                        {
                            firstRule = false;
                            rule += '(' + $(dummyStr2).val() + '|';
                        }
                        else
                        {
                            rule += $(dummyStr2).val() + '|';
                        }
                    }
                }
                else
                {
                    if(j!=numFields)
                    {
                        rule = rule.slice(0, -1);
                        rule += ')*'
                    }
                    else
                    {
                        rule = rule.slice(0, -1);
                        rule += ')'
                    }
                    finishedAlternates = true;
                }
            }

            if(!oneChecked)
            {
                showMessageInDialogBox("Please select at least one alternative from each grid.");
                break;
            }
        }

        if(oneChecked)
        {
            var stat = ""
            if($('#valid').is(':checked'))
                stat = $('#valid').val();
            else if($('#invalid').is(':checked'))
                stat = $('#invalid').val();
            else
                stat = $('#unknown').val();

            if($('#gridUsid').val().length != 0)
                var str = 'rule=' + rule + '&status=' + stat + '&gridid=' + $('#gridUsid').val();
            else
                var str = 'rule=' + rule + '&status=' + stat;

            $.post('/grids/addRule/', str, function(data)
            {
                try
                {
                    if ($(data).find('error').length <= 0)
                    {
                        $('#gridUsid').val(data);
                        $('#rules #explanation').hide();
                        $('#rules').append('<p>' + rule + '</p>');
                    }
                    else
                    {
                        showMessageInDialogBox($(data).find('error').text()); //function from layout.html
                    }
                }
                catch(err)
                {
                    hideLoadingSpinner(loadingDiv);
                    console.log(err);
                }
            });
            showMessageInDialogBox(rule);
        }
	});
});
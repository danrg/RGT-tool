var displayHelp = false;

$(function () {
    $(".helpHover").hide();

    $.get('/profile/displayHelp', function(data) {
        displayHelp = data.getElementsByTagName('htmlData')[0].textContent;

        if (displayHelp === "True") {
            $(".helpHover").each(function (index, value) {
                $(value).tipsy({html: false, gravity: 'w', fade: true});

                $.get('/help/' + value.id, function(data) {
                    var isError = data.getElementsByTagName("error").length > 0;

                    if(!isError) {
                        var helpText = data.getElementsByTagName('htmlData')[0].textContent;

                        $(value).attr('title', helpText);
                    }
                });
            });

            $(".helpHover").show();
        }
    });
});
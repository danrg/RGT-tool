$(document).ready(function () {
    $('.btn-mark-valid').click(predefinedRuleAddButtonHandler);
    $('#btn-add').click(customRuleAddButtonHandler);
    $('input[type=checkbox]').click(selectAllHandler);
    $('#added-rules').on('click', 'a.remove-rule', removeRuleHandler);
});

function predefinedRuleAddButtonHandler() {
    rule = $(this).parent().siblings(':first').html();
    addRule(rule, "Valid");
    $(this).parents('tr').remove();
}

function customRuleAddButtonHandler() {
    var valid = true;
    var allAlternatives = [];
    $('.grid-alternatives').each(function() {
        alternatives = $(this).find('input:checked').not('input[name=select-all]');
        if(alternatives.length > 0) {
            allAlternatives.push(alternatives);
        } else {
            valid = false;
        }
    });

    if(valid) {
        status = $('#status-wrapper input:checked').val();
        rule = createRule(allAlternatives);
        addRule(rule, status);
        $('#alt-list input[type=checkbox]').attr('checked', false);
        $('#alt-list input[value=Valid]').attr('checked', true);
    } else {
        showMessageInDialogBox("Please select at least one alternative from each grid.");
    }
}

function selectAllHandler() {
    var checked = $(this).is(':checked');
    if($(this).attr('name') === 'select-all') {
        $(this).parents("div.container").children("input").attr('checked', checked);
    } else {
        siblings = $(this).siblings("input");
        checkedSiblings = $(this).siblings("input:checked");
        if(siblings.length - checkedSiblings.length == 0) {
            $(this).siblings(".select-all-wrapper").children("input").attr('checked', checked);
        }
    }
}

function removeRuleHandler() {
    $(this).parents('tr').remove();
    if($('#added-rules > tbody').children().length === 0) {
        $('#added-rules').hide();
        $('#explanation').show();
    }
}

function addRule(ruleStr, status) {
    $('#rules #explanation').hide();
    ruleCell = '<td>' + ruleStr + '</td>';
    statusCell = '<td>' + status + '</td>';
    removeCell = '<td><a href="javascript:void(0);" class="remove-rule">Remove</a></td>';
    inputCell = '<input type="hidden" name="rules" value="' + ruleStr + '" />';
    $('#added-rules tbody').append('<tr>' + ruleCell + statusCell + removeCell + inputCell + '</tr>');
    $('#added-rules').show();
}

function createRule(alternatives) {
    andRules = [];
    $.each(alternatives, function() {
       if($(this).length == 1) {
           andRules.push($(this).val());
       } else {
           orRules = [];
           $.each($(this), function() {
              orRules.push($(this).val());
           });
           andRules.push(orRules.join("|"));
       }
    });
    return "(" + andRules.join(")*(") + ")";
}
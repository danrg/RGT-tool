$(document).ready(function () {
    $('.btn-mark-valid').click(predefinedRuleAddButtonHandler);
    $('#btn-add').click(customRuleAddButtonHandler);
    $('input[type=checkbox]').click(selectAllHandler);
    $('#added-rules').on('click', 'a.remove-rule', removeRuleHandler);
});

var addedRules = [];

function Rule(ruleStr, status) {
    this.ruleStr = ruleStr;
    this.status = status;
    this.compositions = [];
}

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
    removeRule($(this));
}

function removeRule(ruleElement) {
    ruleElement.parents('tr').remove();
    if($('#added-rules > tbody').children().length === 0) {
        $('#added-rules').hide();
        $('#explanation').show();
    }
}

function createNewRule(ruleStr, status) {
    rule = new Rule(ruleStr, status);
    if(ruleStr.indexOf('|') < 0) {
        rule.compositions.push(ruleStr);
    } else {
        listOfLists = []
        words = ruleStr.split('*');
        for (var i = 0; i < words.length; i++) {
            var word = words[i].substring(1, words[i].length - 1);
            listOfLists.push(word.split("|"));
        }
        cartesianProducts = cartesianProductOf.apply(this, listOfLists);
        for (var i = 0; i < cartesianProducts.length; i++) {
            product = cartesianProducts[i];
            ruleComposition = '(' + product.join(')*(') + ')';
            rule.compositions.push(ruleComposition)
        }
    }
    return rule;
}

function findConflictingRule(rule) {
    for (var ruleIndex = 0; ruleIndex < addedRules.length; ruleIndex++) {
        existingRule = addedRules[ruleIndex];
        for (var i = 0; i < rule.compositions.length; i++) {
            composition = rule.compositions[i];
            for (var j = 0; j < existingRule.compositions.length; j++) {
                existingComposition = existingRule.compositions[j];
                if (composition == existingComposition) {
                    return existingRule;
                }
            }
        }
    }
    return null;
}

function addRule(ruleStr, status) {
    rule = createNewRule(ruleStr, status);
    conflict = findConflictingRule(rule);
    if(conflict == null) {
        doAddRule(rule);
    } else {
        buttons = {
            'Add anyway': function() {
                doAddRule(rule);
                $(this).dialog("close");
            },
            'Overwrite existing rule': function() {
                ruleElement = $('tr').find('td:contains('+ conflict.ruleStr+')');
                removeRule(ruleElement);
                doAddRule(rule);
                $(this).dialog("close");
            },
            'Cancel': function() {
                $(this).dialog("close");
            }
        };
        overlapsOrConflicts = status == "Valid" ? "overlaps" : "conflicts";
        text = 'You are trying to add rule ' + ruleStr + '. This ' + overlapsOrConflicts + ' with rule '
            + conflict.ruleStr + '. What would you like to do?';
        showMessageInBox(text, buttons)
    }
}

function doAddRule(rule) {
    addedRules.push(rule);
    $('#rules #explanation').hide();
    ruleCell = '<td>' + rule.ruleStr + '</td>';
    statusCell = '<td>' + rule.status + '</td>';
    removeCell = '<td><a href="javascript:void(0);" class="remove-rule">Remove</a></td>';
    inputs = '<input type="hidden" name="rules" value="' + rule.ruleStr + '" />' +
        '<input type="hidden" name="statuses" value="' + rule.status + '" />"';
    $('#added-rules tbody').append('<tr>' + ruleCell + statusCell + removeCell + inputs + '</tr>');
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

// http://stackoverflow.com/a/5860190/509671
function cartesianProductOf() {
  return Array.prototype.reduce.call(arguments, function(a, b) {
    var ret = [];
    a.forEach(function(a) {
      b.forEach(function(b) {
        ret.push(a.concat([b]));
      });
    });
    return ret;
  }, [[]]);
}
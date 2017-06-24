from django import template

register = template.Library()


@register.filter
def divide_by(value, arg):
    """
    Returns the result of the division of value with arg.
    """
    result = 0
    try:
        result = value / arg
    except:
        # error in division
        pass
    return result


@register.filter
def sort_dict_by_key(dictionary):
    """
    Returns the dictionary sorted as list [(), (),].
    """
    return sorted(dictionary.items()) if dictionary else None


@register.filter
def get_value_of_dict(dictionary, key):
    """
    Returns the value of the dictionary with the given key.
    """
    value = 0
    try:
        value = dictionary[str(key)]
    except KeyError:
        pass
    return value


@register.filter
def get_left_concern_value(dictionary, index):
    """
    Returns the value of the left concern name of the pair found in dictionary with key = index.
    
    This is a special filter which is used only in extracting the left concern name of the dictionary.
    The dictionary name used is "concerns_data_in_pairs" which is constructed in:
        /gridMng/wizard/views.py
    as extra context data for step 4 and step 5. The format of the dictionary is:
        concern_data_in_pairs = {
            "1" : (concern_left_name, concern_right_name),
            "2" : (concern_left_name, concern_right_name),
            ...
        }
    """
    value = None
    try:
        # The index 0 being used, is in order to extract the first value of the tuple which gives the
        # left concern name.
        value = dictionary[str(index)][0]
    except KeyError:
        pass
    return value


@register.filter
def get_right_concern_value(dictionary, index):
    """
    Returns the value of the right concern name of the pair found in dictionary with key = index.

    This is a special filter which is used only in extracting the right concern name of the dictionary.
    The dictionary name used is "concerns_data_in_pairs" which is constructed in:
        /gridMng/wizard/views.py
    as extra context data for step 4 and step 5. The format of the dictionary is:
        concern_data_in_pairs = {
            "1" : (concern_left_name, concern_right_name),
            "2" : (concern_left_name, concern_right_name),
            ...
        }
    """
    value = None
    try:
        # The index 1 being used, is in order to extract the second value of the tuple which gives the
        # right concern name.
        value = dictionary[str(index)][1]
    except KeyError:
        pass
    return value


@register.filter
def get_range(value):
    """
    Returns the range of the value.
    """
    return range(value)


@register.filter
def get_non_hidden_fields(form):
    """
    Returns all the visible fields of the form.
    """
    return form.visible_fields()


@register.filter
def get_hidden_fields(form):
    """
    Returns all the hidden fields of the form.
    """
    return form.hidden_fields()


@register.filter
def concat(value1, value2):
    """
    Returns the concatenation of numbers value1 and value2 as string.
    """
    return "%d%d" % (value1, value2)

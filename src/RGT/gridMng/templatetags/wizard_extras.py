from django import template

register = template.Library()

@register.filter
def divide_by(value, arg):
    result = 0
    try:
        result = value / arg
    except:
        # error in division
        pass
    return result

@register.filter
def sort_dict_by_key(dictionary):
    # return the dictionary sorted as list [(), ()]
    return sorted(dictionary.items()) if dictionary else None

@register.filter
def get_value_of_dict(dictionary, index):
    # return the value of the dictionary with key 'index'
    return dictionary[str(index)]

@register.filter
def get_left_concern_value(dictionary, index):
    # return the value of the dictionary with key 'index'
    return dictionary[str(index)][0]

@register.filter
def get_right_concern_value(dictionary, index):
    # return the value of the dictionary with key 'index'
    return dictionary[str(index)][1]

@register.filter
def divide_and_get_left_concern_value(dictionary, index):
    # return the value of the dictionary with key 'index'
    return dictionary[str(index/2)][0]

@register.filter
def divide_and_get_right_concern_value(dictionary, index):
    # return the value of the dictionary with key 'index'
    return dictionary[str(index/2)][1]

@register.filter
def get_range(value):
    # return the range of the value
    return range(value)
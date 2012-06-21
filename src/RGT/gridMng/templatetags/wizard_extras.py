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
    # return list as [(), ()]
    return sorted(dictionary.items()) if dictionary else None

@register.filter
def get_value_of_dict(dictionary, index):
    return dictionary[index]

@register.filter
def get_range(value):
    return range(value)
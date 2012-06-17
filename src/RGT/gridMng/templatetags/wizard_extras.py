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
def sort_dict_by_key(d):
    # return list as [(), ()]
    return sorted(d.items()) if d else None
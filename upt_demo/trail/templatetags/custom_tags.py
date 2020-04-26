from django import template

register = template.Library()


@register.filter()
def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

@register.filter()
def get_dict_item(dictionary, key):
    return dictionary.get(key)



from django import template

register = template.Library()

@register.simple_tag
def fixtags(content):
    tags = {
        '&lt;sub&gt;': '<sub>',
        '&lt;/sub&gt;': '</sub>',
        '&lt;ins&gt;': '<ins>',
        '&lt;/ins&gt;': '</ins>',
        '&lt;del&gt;': '<del>',
        '&lt;/del&gt;': '</del>',
    }
    for old, new in tags.items():
        content = content.replace(old, new)
    return content
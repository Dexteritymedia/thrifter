from django import template

from app.models.contact import FAQ

register = template.Library()

@register.inclusion_tag("misc/faqs.html", takes_context=True)
def faqs_tag(context):
    faqs = FAQ.objects.all()
    context['faqs'] = faqs
    return context


@register.simple_tag
def current_title():
    return 'Title'

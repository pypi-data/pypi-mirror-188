from django.template import Library, loader
from webuild.forms import ContactForm

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.simple_tag(takes_context=True)
def hero(context):
    t = loader.get_template("webuild/_hero.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def contact(context):
    t = loader.get_template("webuild/_contact.html")
    context.update({
        'form': ContactForm(),
        'post_message': context.get('post_message', None),
    })
    logger.info(context)
    return t.render(context.flatten())
from django import template
from django.core import urlresolvers


register = template.Library()


class AdminLinkResolver(template.Node):
    def __init__(self, model_instance):
        self.model = template.Variable(model_instance)

    def render(self, context):
        try:
            model = self.model.resolve(context)
            ref = urlresolvers.reverse(
                'admin:%s_%s_change' % (model._meta.app_label,
                                        model.__class__.__name__.lower()),
                args=(model.id,))
        except:
            ref = ""
        return ref


@register.tag(name='get_admin_link')
def get_admin_link(parser, token):
    try:
        tag_name, model_object = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '''%r  tag requires a single object
            from your application models''' % token.contents.split()[0])
    return AdminLinkResolver(model_object)

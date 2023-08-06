from component_tags import template
from django.apps import apps

register = template.Library()


@register.tag()
class List(template.Component):
    """
    A flexible component to display a HTMX enabled list.
    """

    editable = template.Attribute(default=True)
    deletable = template.Attribute(default=True)
    model = template.Attribute(required=True)
    fields = []

    class Meta:
        template_name = "core/components/list.html"

    def get_queryset(self):
        app_label, model_name = self.attrs["model"].var.split(".")
        model = apps.get_model(app_label, model_name)
        return model.objects.all()

    def get_context_data(self, context):
        objects = self.get_queryset()
        context.update({"objects": objects})
        return super().get_context_data(context)

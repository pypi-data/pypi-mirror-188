from crispy_forms.layout import Field
from crispy_forms.utils import TEMPLATE_PACK


class TimeSelector(Field):
    """Crispy Widget that provides a time input, the current time with seconds,
    and two buttons that increase/decrease the time by a unit, per default 15min.
    """

    template = "bootstrap5/layout/timeselector.html"

    def __init__(self, *args, show_current_time=False, units=15, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_current_time = show_current_time
        self.units = units

    def render(
        self,
        form,
        form_style,
        context,
        template_pack=TEMPLATE_PACK,
        extra_context=None,
        **kwargs
    ):
        if extra_context is None:
            extra_context = {}
        extra_context["show_current_time"] = self.show_current_time
        extra_context["units"] = self.units
        extra_context["step"] = self.units * 60
        return super().render(
            form, form_style, context, template_pack, extra_context, **kwargs
        )

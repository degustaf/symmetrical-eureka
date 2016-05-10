"""
Renderers that extend bootstrap renderers.
"""

from re import sub

from django.forms import DateInput, Select, TextInput

from bootstrap3.renderers import FieldRenderer


class AbilityScoreFieldRenderer(FieldRenderer):
    """
    Class to render Ability Score input fields.
    """
    def __init__(self, field, *args, **kwargs):
        super(AbilityScoreFieldRenderer, self).__init__(field, *args, **kwargs)
        self.mod_id = sub(r'_', r'_mod_', self.field.id_for_label)

    def make_input_group(self, html):
        if (self.addon_before or self.addon_after) and\
                isinstance(self.widget, (TextInput, DateInput, Select)):
            before = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_before) if self.addon_before else ''
            if self.addon_after:
                after = '<div class="{}" id="{}">{}</div>'.format(
                    'ability-score-mod badge', self.mod_id, self.addon_after)
                after = '<div class="as-mod-padding">{addon}</div>'.format(
                    addon=after)
            else:
                after = ''
            html = '{before}{html}{after}'.format(
                before=before,
                after=after,
                html=html
                )
        return html

    def wrap_label_and_field(self, html):
        html = '<div>{}</div>'.format(html)
        return super(AbilityScoreFieldRenderer, self).wrap_label_and_field(
            html)

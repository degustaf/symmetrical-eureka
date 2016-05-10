"""
Specialized template tags.
"""


from django import template
from django.utils.html import format_html

from bootstrap3.forms import render_field

from ..models import Character


def _bs_ability_score_field(*args, **kwargs):
    """
    Wrapper around bootstrap_field with ability score arguments.
    """
    # if "form_group_class" in kwargs:
    #     kwargs["form_group_class"] = "col-sm-2 col-xs-4 ability-score-block"\
    #         + kwargs["form_group_class"]
    # else:
    #     kwargs["form_group_class"] = "col-sm-2 col-xs-4 ability-score-block"

    kwargs["form_group_class"] = "col-sm-2 col-xs-4 ability-score-block"
    kwargs["addon_after"] = " "
    kwargs["layout"] = "ability_scores"

    return render_field(*args, **kwargs)


def _bs_ability_score_display(player_character, ability_score):
    """
    Render an html element to display field.
    """
    # pylint: disable=protected-access
    field = player_character._meta.get_field(ability_score)
    val = getattr(player_character, ability_score)
    mod = "{:+d}".format(Character.ability_score_mod(val))

    html = format_html("""<div class="col-sm-2 col-xs-4 ability-score-block">
                    <div>
                        <label class="control-label" for="id_{name}">
                            {}
                        </label>
                    <p class="ability-score" id="id_{name}">{val}</p>
                    <input class="form-control invisible" id="id_{name}"
                        min="0" name="{name}" title="" type="number"
                        value={val}>
                    <div class="as-mod-padding">
                        <p class="{}" id="id_mod_{name}">{}
                </p></div></div></div>""",
                       field.verbose_name.capitalize(),
                       "ability-score-mod badge",
                       mod,
                       val=val,
                       name=field.name)
    return html


# pylint: disable=invalid-name
register = template.Library()


@register.simple_tag
def bs_ability_score_field(*args, **kwargs):
    """ Wrapper around _bs_ability_score for templates."""
    return _bs_ability_score_field(*args, **kwargs)


@register.simple_tag
def bs_ability_score_display(player_character, ability_score):
    """ Wrapper around _bs_ability_score_display for templates."""
    return _bs_ability_score_display(player_character, ability_score)

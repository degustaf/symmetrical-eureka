"""
Specialized template tags.
"""


# from pdb import set_trace
from django import template
from django.utils.html import format_html

from bootstrap3.forms import render_field

from ..models import AbilityScores


def _bs_ability_score_field(*args, **kwargs):
    """
    Wrapper around bootstrap_field with ability score arguments.
    """
    kwargs["form_group_class"] = "col-sm-2 col-xs-4 value-block" +\
        " ability-score-block"
    kwargs["addon_after"] = " "
    kwargs["layout"] = "ability_scores"

    return render_field(*args, **kwargs)


def _bs_skills_field(*args, **kwargs):
    """
    Wrapper around bootstrap_field with skills arguments.
    """
    kwargs["form_group_class"] = "col-sm-2 col-xs-4 value-block" +\
        " skills-block"
    kwargs["addon_before"] = " "
    kwargs["layout"] = "skills"

    return render_field(*args, **kwargs)


def _bs_ability_score_display(ability_score):
    """
    Render an html element to display field.
    """
    field = AbilityScores.WHICH_KEY_2_ENG[ability_score.which]
    val = ability_score.value
    mod = "{:+d}".format(AbilityScores.ability_score_mod(val))

    html = format_html("""<div class="col-sm-2 col-xs-4 ability-score-block value-block">
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
                       field.capitalize(),
                       "ability-score-mod badge",
                       mod,
                       val=val,
                       name=field)
    return html


def _bs_saving_throw_display(ability_score):
    """
    Render an html element to display field.
    """
    field = AbilityScores.WHICH_KEY_2_ENG[ability_score.which]
    val = "{:+d}".format(ability_score.saving_throw)\
        if ability_score.value else ""
    prof = "proficient" if ability_score.proficient else "unproficient"

    html = format_html("""<div class="col-sm-2 col-xs-4 value-block">
                    <div>
                        <label class="control-label" for="id_sav_{name}">
                            {}
                        </label>
                    <p class="sav-score" id="id_sav_{name}">{val}</p>
                    <div class="as-mod-padding">
                        <p class="{}" id="id_sav_prof_{name}"></p>
                    </div></div></div>""",
                       field.capitalize(),
                       prof,
                       val=val,
                       name=field)
    return html


# pylint: disable=invalid-name
register = template.Library()


@register.simple_tag
def bs_ability_score_field(*args, **kwargs):
    """ Wrapper around _bs_ability_score for templates."""
    return _bs_ability_score_field(*args, **kwargs)


@register.simple_tag
def bs_ability_score_display(ability_score):
    """ Wrapper around _bs_ability_score_display for templates."""
    return _bs_ability_score_display(ability_score)


@register.simple_tag
def bs_saving_throw_display(ability_score):
    """ Wrapper around _bs_saving_throw_display for templates."""
    return _bs_saving_throw_display(ability_score)


@register.simple_tag
def bs_skills_field(skill):
    """ Wrapper around _bs_skills_field for templates."""
    return _bs_skills_field(skill)

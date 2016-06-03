/*jslint browser: true*/
/*global $, document*/

function get_csrf_token() {
    var cookie = document.cookie;
    var start = cookie.indexOf('csrftoken=');
    if(start === -1) {
        return "";
    }
    var end = cookie.indexOf(';', start);
    start += 'csrftoken='.length;
    if(end === -1) {
        return cookie.substring(start);
    }
    return cookie.substring(start, end);
}

function adjust_mod(data, mod_id) {
    var mod = data;
    if(mod >= 0) {
        mod = "+" + mod;
    }
    $("#" + mod_id).text(mod);
}

function toggle_fieldset() {
    $(this).parent().toggleClass('toggle-border');
    $(this).siblings().toggle();
    $(this).children('.glyphicon').toggleClass('glyphicon-minus').toggleClass('glyphicon-plus');
}

function adjust_skills(data) {
    var key, proficient;
    for (key in data) {
        if (data.hasOwnProperty(key)) {
            proficient = $("#id_" + key.replace(/ /g, "_") + "-proficient").prop("checked");
            adjust_mod(data[key] + 2 * proficient, "id_mod_" + key.replace(/ /g, "_") + "-proficient");
        }
    }
}

function get_ability_score_mod() {
    var value = $(this).val();
    var proficient_id = this.id.replace("_", "_sav_prof_").replace("-value", "");
    var proficient = $("#" + proficient_id).hasClass("proficient");
    var mod_id = this.id.replace("_", "_mod_").replace(/ /g, "_");
    var sav_id = this.id.replace("_", "_sav_").replace("-value", "");
    var which = this.getAttribute("name").split("-")[0];

    $.get("http://degustaf.pythonanywhere.com/SymmetricalEureka/api/AbilityScores/ability_score_mod",
            {"ability_score": value, "proficient": proficient, "which": which})
        .done( function(data) {
            adjust_mod(data.ability_score_mod, mod_id);
            adjust_mod(data.abs_saving_throw, sav_id);
            adjust_skills(data.abs_skills_bonus);
        });
}

function toggle_p_with_input() {
    $('p#' + this.id).addClass('invisible');
    $('input#' + this.id).removeClass('invisible').focus();
}

function update_ability_score() {
    var ability_score = $(this).attr("name");
    var mod_id = this.id.replace("_", "_mod_").replace(/ /g, "_");
    var sav_id = this.id.replace("_", "_sav_");
    var url = "http://degustaf.pythonanywhere.com/SymmetricalEureka/api/" + $("#uuid").text() + "/AbilityScores/" + ability_score;
    var p_elmnt = $("p#id_" + ability_score);
    var input_elmnt = $("input#id_" + ability_score);

    var post_data = {'csrfmiddlewaretoken': get_csrf_token(),
                     'value': $(this).val()};

    $.post(url, post_data)
        .done(function(data) {
            adjust_mod(data.ability_score_mod, mod_id);
            adjust_mod(data.saving_throw, sav_id);
        })
        .fail(function() {
            input_elmnt.val(p_elmnt.val());
        })
        .always(function(data) {
            p_elmnt.text(data[ability_score]).removeClass('invisible');
            input_elmnt.val(data[ability_score]).addClass('invisible');
        });
}

function update_skills_bonus() {
    // var skill = $(this).attr("name");
    var mod_id = this.id.replace("_", "_mod_");
    var bonus = Number($("#" + mod_id).text());
    bonus += $(this).prop("checked") ? 2: -2;
    adjust_mod(bonus, mod_id);
}

$(document).ready(function() {
    $('legend').click(toggle_fieldset);
    $('.ability-score').click(toggle_p_with_input);
});

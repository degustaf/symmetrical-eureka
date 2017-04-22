/*jslint browser: true*/
/*global $, document, api_url, class_api_url*/

var filters = {};

function make_table_sortable() {
    $.fn.dataTable.ext.type.order['num-pre'] = function(d) {
        if(d === 'Cantrip') {
            return 0;
        }
        return d;
    };

    $('#spell_table').DataTable( {
        "paging": false,
        "searching": false,
        "info": false,
        "columnDefs": [ {
            "type": "num",
            "targets": 2
        } ]
    } );
}

function combine_school_level(level, school, ritual) {
    var ret;
    switch(level) {
        case "Cantrip":
            ret = school + " Cantrip";
            break;
        case 1:
            ret = "1st level " + school;
            break;
        case 2:
            ret = "2nd level " + school;
            break;
        case 3:
            ret = "3rd level " + school;
            break;
        default:
            ret = level + "th level " + school;
    }
    if(ritual) {
        ret = ret + " (ritual)";
    }
    return ret;
}

function build_modal(data) {
    $("#ModalTitle").text(data.name);
    $("#school").text(combine_school_level(data.level, data.school, data.ritual));
    $("#casting_time").text(data.casting_time);
    $("#duration").text(data.duration);
    $("#range").text(data.spell_range);
    $("#components").text(data.components);
    $("#description").text(data.description);
    $("#source").text(data.page);
    $("#materials").text(data.material_components);
    if(data.material_components === "") {
        $("#mat_comp").addClass("hidden");
    } else {
        $("#mat_comp").removeClass("hidden");
    }

    $("div.modal").modal('show');
}

function ajax_modal() {
    $("tbody > tr").click(function(evt) {
		var cell=$(evt.target).closest('td');
		if( cell.index()>0){
			var name = $(this).find(".name").text();
			$.get(api_url + encodeURI(name)).done(build_modal);
		}
    });
    $("div.modal").click(function() {
        $("div.modal").modal('hide');
    });
}

function apply_filters() {
    $("#spell_table > tbody > tr").each(function() {
        var name = $(this).find(".name").text();
        var lvl = $(this).find(".lvl").text();
        if((filters.cls === undefined ||
            filters.cls.spells[name] !== undefined) &&
           (filters.lvl === undefined ||
            filters.lvl === lvl)) {
            $(this).removeClass("hidden");
        } else {
            $(this).addClass("hidden");
        }
    });
}

function filter_classes() {
    $("a.class_filter").click(function() {
        var re = /class_filter_(.+)$/;
        var id = $(this).prop('id');
        var cls = id.match(re)[1];
        if( cls === "any" ) {
            $("#active_class").text("Class");
            if(filters.hasOwnProperty('cls')) {
                delete filters.cls;
            }
            apply_filters();
        } else if(filters.cls === undefined || cls !== filters.cls.cls) {
            $("#active_class").text($("#"+id).text());
            $.get(class_api_url + cls).done( function(data) {
                filters.cls = {"cls": cls,
                               "spells": data.reduce(function(acc, x) {
                                   acc[x.spell] = true;
                                   return acc;
                               }, {})};
                apply_filters();
            });
        }
    });
}

function filter_levels() {
    $("a.level_filter").click(function() {
        var re = /level_filter_(.+)$/;
        var id = $(this).prop('id');
        var lvl = id.match(re)[1];
        if( lvl === "any" ) {
            $("#active_level").text("Level");
            if(filters.hasOwnProperty('lvl')) {
                delete filters.lvl;
            }
        } else {
            $("#active_level").text($("#"+id).text());
            filters.lvl = lvl;
        }
        apply_filters();
    });
}

$(document).ready(function() {
    make_table_sortable();
    ajax_modal();
    filter_classes();
    filter_levels();
} );

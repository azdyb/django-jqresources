django.jQuery(document).ready(function() {
    
    django.jQuery("td.field-version input[type=text], td.field-path input[type=text]").attr("disabled", "disabled");
    django.jQuery("#versions-group thead th:last-child").hide();
    django.jQuery("#versions-group tbody td:last-child").hide();

    django.jQuery("#versions-group h2").append("<span class=\"edit-versions\" ><a>" + gettext("Edit") + "</a></span>");
    django.jQuery("#versions-group span.edit-versions a").click(function(event) {
        django.jQuery("#versions-group thead th:last-child").show();
        django.jQuery("#versions-group tbody td:last-child").show();
        django.jQuery("td.field-version input[type=text], td.field-path input[type=text]").removeAttr("disabled");
        django.jQuery("#versions-group span.edit-versions").remove();
    });
    
    django.jQuery("input[type=submit]").click(function(event) {
        django.jQuery("td.field-version input[type=text], td.field-path input[type=text]").each(function() {
            var $this = django.jQuery(this);
            if ($this.attr("disabled")) {
                $this.removeAttr("disabled");
                $this.addClass("disabled");
            }
        });
    });
    
    django.jQuery("input[name=have_default_version]").change(toggleHasDefault).change();    
});

function toggleHasDefault() {
    if (django.jQuery("input[name=have_default_version]").attr("checked")) {
        var inputs = django.jQuery("input[name=default_version]");
        django.jQuery("#versions-group thead th:first-child").show();
        django.jQuery("#versions-group tbody td:first-child").show();
        inputs.parents("td.field-Default").show();
    } else {
        var inputs = django.jQuery("input[name=default_version]");
        inputs.parents("td.field-Default").hide();
        django.jQuery("#versions-group thead th:first-child").hide();
        django.jQuery("#versions-group tbody td:first-child").hide();
    }
}
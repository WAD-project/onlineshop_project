$( function() {
    var availableProducts = [
        {% for pdt in all_products %}
            "{{pdt}}",
        {%endfor%}
    ];
    $( "#pdt" ).autocomplete({
        source: availableProducts
    });
} );
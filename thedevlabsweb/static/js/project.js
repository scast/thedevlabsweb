/* Project specific Javascript goes here. */

// Django & CSRF play nice.
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/// Discover button handler.
var discoverTemplate = _.template($('#discover-list').html());
var discoverButton = function() {
    var query = $('input[name=q]').val();
    $.post('/search/', {
        "q": query
    }, function(data) {
        $('#discover-results').html(discoverTemplate({
            'results': data
        }));
        $('.tweet').linkify();
    });

};


$(function() {
    $('.tweet').linkify({
        'linkAttributes': {
            'data-track': 'url'
        }
    });

    $('#submit-discover').click(discoverButton);

});

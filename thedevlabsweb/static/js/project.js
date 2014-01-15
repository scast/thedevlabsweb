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

/// Whats up button handler.
var supTemplate = _.template($('#sup-list').html());
var supButton = function() {
    var query = $('input[name=q]').val();
    $.post('/search/', {
        "q": query
    }, function(data) {
        $('#sup-results').html(supTemplate({
            'results': data
        }));
        $('.tweet').linkify();
    });

};

// Main.
$(function() {
    $('#submit-sup').click(supButton);
    $('#sup-results').on('click', '.linkified' , function(e) {
        console.log("Valor", $(this).attr('href'))
        return false;
    });
});

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

var supSelectLink = function(e) {
    var url = $(this).attr('href');
    $.post('/recommender/add/', {'url': url}, function(data) {
        if (data.status === 'ok') {
            $('#sup-twitter').modal('hide');
            console.log(data);
        }
    });
    return false;
}

// Discover button enable/disable

var $discover = $('#discover');
var $up = $('#discover-like');
var $down = $('#discover-dislike');

var discoverEnable = function() {
    $up.addClass('disabled');
    $down.addClass('disabled');
    $discover.removeClass('disabled');

}

var discoverScoreEnable = function() {
    $up.removeClass('disabled');
    $down.removeClass('disabled');
    $discover.addClass('disabled');
}

var discoverClick = function() {
    discoverScoreEnable();
}

var discoverHandleScore = function() {
    discoverEnable();
    console.log('contacting server...');
}


// Main.
$(function() {
    discoverEnable();
    $('#submit-sup').click(supButton);
    $('#sup-results').on('click', '.linkified' , supSelectLink);
    $discover.click(discoverClick);
    $up.click(discoverHandleScore);
    $down.click(discoverHandleScore);
});

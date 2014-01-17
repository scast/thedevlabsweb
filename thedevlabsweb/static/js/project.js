(function() {
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


    // Discover button enable/disable
    var $discover = $('#discover');
    var $up = $('#discover-like');
    var $down = $('#discover-dislike');

    var discoverEnable = function() {
        $up.addClass('disabled');
        $down.addClass('disabled');
        $discover.removeClass('disabled');

    };

    var discoverScoreEnable = function() {
        $up.removeClass('disabled');
        $down.removeClass('disabled');
        $discover.addClass('disabled');
    };

    var loadSite = function(pk, url) {
        $up.attr('data-pk', pk);
        $down.attr('data-pk', pk);
        $('#website').html(url);
        discoverScoreEnable();
    };


    var discoverClick = function() {
        $.post('/recommender/discover/', function(data) {
            if (data.status === 'ok') {
                console.log(data.url)
                discoverScoreEnable();
                loadSite(data.pk, data.url);
            }
            else if (data.status === 'done') {
                console.log('No hay mas sitios web')
            }
            else {
                console.log('Error.')
            }
        });
    };


    var upClick = function() {
        console.log('up');
        $up.addClass('disabled');
        $down.removeClass('disabled')
        var pk= $up.attr('data-pk');
        $.post('/recommender/discover/'+pk+'/like/');
    };

    var downClick = function() {
        console.log('down');
        $down.addClass('disabled');
        $up.removeClass('disabled')
        var pk= $down.attr('data-pk');
        $.post('/recommender/discover/'+pk+'/dislike/');
    };

    var discoverHandleScore = function(value) {
        return function() {
            discoverEnable();
            console.log('contacting server...');
            if (value == 1)
                upClick()
            else
                downClick()
        }

    };


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
                loadSite(data.pk, data.url);
                console.log(data);
            }
        });
        return false;
    };

    // Main.
    $(function() {
        discoverEnable();
        $('#submit-sup').click(supButton);
        $('#sup-results').on('click', '.linkified' , supSelectLink);
        $discover.click(discoverClick);
        $up.click(discoverHandleScore(1));
        $down.click(discoverHandleScore(-1));
    });

})()

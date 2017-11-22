'use strict';

var App = {};

App = {
    scrollspy: function scrollspy() {
        $('.scrollspy').scrollSpy();
    },
    loaded: function loaded() {
        var $body = $('body');
        var spinnerContainer = $('.spinner-container');

        // Locking body's scrolling
        $body.addClass('locked');
        $(window).on('load', function () {
            // Unlocking body's scrolling and hiding the spinner
            $body.removeClass('locked');
            spinnerContainer.addClass('hide-spinner');
            setTimeout(function () {
                spinnerContainer.hide();
            }, 400);
        });
    }
};

$(function () {
    App.scrollspy();
    App.loaded();
});

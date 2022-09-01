$('.carousel-item').click(function() {
    console.log('clicked')
    if (typeof $(this).attr('href') !== 'undefined') {
        window.location = $(this).attr('href');
    }
});

$(".resnav-menu").click(function() {
    $(".resnav").toggleClass("active");
})
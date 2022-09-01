$('.approve').click(function() {
    let id = $(this).attr('id');
    let data = {
        'id': id,
        'points': $('#points-' + id).val()
    }
    $.ajax({
        url: '/admin/receipts/approve/',
        type: 'POST',
        data: data,
        success: function(response) {
            console.log(response);
        }
    });
    console.log('a')
});
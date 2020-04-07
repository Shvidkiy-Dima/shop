$(document).on('click', '[data-action="detail-product"]', function() {
    $.ajax({
        url: '/api/detail-product/',
        method: 'GET',
        data: {'pk': $(this).data('id')},
        success: function(json) {
              $("#base-shop-modal").html(json['html'])
              $('#base-shop-modal').modal('show')
        },
        error: function(data) {
            console.log('Invalid')
        },
    })

})

$('#base-shop-modal').on('hide.bs.modal', function() {
    $("#base-shop-modal").html('')
})


$(document).on('change', '#size-change-product', function(obj) {
    console.log(obj)
    var variant_id = $(this).val()
    var selected = $(this).find('option:selected')
    var variant_price = selected.data('price')

    $('[data-action="order-product"]').attr('data-id', variant_id)
    $('[data-id="variant-price"]').text(variant_price)
})






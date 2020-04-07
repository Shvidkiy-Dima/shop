$(document).on('click', '[data-action="order-product"]', function() {
    var id = $(this).data('id')
    var element = $(this).closest('[data-id="body-product-cart"]')
    $.ajax({
        url: '/api/cart/put/',
        method: 'POST',
        data: {'id': id},
        success: function(data) {

            $('#cart-counter').text(data['count'])

            element.find('[data-id="cart-counter-product"]').text(data['count_order'])
            element.find('[data-id="cart-variant-price"]').text(data['price'])

            $('#base-shop-modal').modal('hide')
            console.log(data['extra'])
            if (data['extra'][0]) {
                element.find('[data-id="cart-product-exceed"]').text('В наличие только ' + data['extra'][1])
            }
        },

    })
})

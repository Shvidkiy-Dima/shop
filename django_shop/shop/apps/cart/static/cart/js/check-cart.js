$('#my-cart').on('click', function(){
        $.ajax({
            url: '/api/cart/check/',
            method: 'GET',
            success: function(json) {
              $("#my-cart-modal").html(json['html'])
              $('#my-cart-modal').modal('show')

            },

        })


})


$('#my-cart-modal').on('hide.bs.modal', function() {
    $("#my-cart-modal").html('')



})

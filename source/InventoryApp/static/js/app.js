jQuery(document).ready(function($) {
    $('.no_of_items').val($('.balance-js').text());

    setTimeout(function() {
        $(".alert:visible").fadeOut('slow');
    }, 2000);

    $('.increase-stock').click(function() {
        var stock_val = parseInt($('.no_of_items').val());
        var remaining = parseInt($('.balance-js').text());
        var stock_in_out = $('input[name="stock_in_out"]:checked').val();

        if (isNaN(stock_val)) {
            stock_val = 0;
        }

        if ((stock_val !== '' && stock_val < remaining) || stock_in_out == 'stock_in') {
            $('.no_of_items').val((stock_val+1))
        }
    });

    $('.decrease-stock').click(function() {
        var stock_val = parseInt($('.no_of_items').val());
        var max_unit = parseInt($('.no_of_items').data('max-unit'));
        var stock_in_out = $('input[name="stock_in_out"]:checked').val();

        if (isNaN(stock_val)) {
            stock_val = 0;
        }

        if (stock_val !== '' && stock_val !== 0 && (max_unit < stock_val || stock_in_out == 'stock_out')) {
            $('.no_of_items').val((stock_val-1))
        }
    });

    $('.stock_in_out').click(function() {
        $('.stock-in-js').hide();
        $('.stock-out-js').hide();

        if ($(this).val() == 'stock_in') {
            $('.stock-in-js').show();
        } else {
            $('.stock-out-js').show();
        }
    });

    $('.cost_per_unit_select').change(function() {
        var total_units = $('.cost_per_unit_select option:selected').attr('data-total-units')
        $('.balance-js').text(total_units);
    });
});

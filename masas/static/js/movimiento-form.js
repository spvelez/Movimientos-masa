$(function () {
    function addRow(table, template) {
        var count = table.data('rowcount');
        if (!count) {
            count = table.children('tbody').children('tr').length;
        }

        var html = template.replace(/\{i\}/g, count);
        table.children('tbody').append(html);

        table.data('rowcount', ++count);
    };

    $('form').on('click', '.remove-row', function () {
        $(this).parents('tr').remove();
        return false;
    });

    $('.add-row').click(function () {
        var table = $(this).data('target'),
            template = $($(this).data('template')).html();

        addRow($(table), template);
    });
});
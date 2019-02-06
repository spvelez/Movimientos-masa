$(document).foundation();
$(document).ready(function () {
    $('body').on('click', '.delete-confirm', function () {
        if (confirm('¿Deseas eliminar este registro?')) {
            var form = document.createElement('form');
            form.action = this.href;
            form.method = 'post';
            $(form).appendTo('body');
            form.submit();
        }

        return false;
    });

    if ($.dynatableSetup) {
        $.dynatableSetup({
            inputs: {
                paginationClass: 'pagination dynatable-pagination',
                paginationLinkClass: 'dynatable-page-link',
                paginationPrevClass: 'pagination-previous',
                paginationNextClass: 'pagination-next',
                paginationDisabledClass: 'disabled',
                paginationPrev: 'Anterior',
                paginationNext: 'Siguiente',
                searchText: 'Buscar: ',
                perPageText: 'Mostrar: ',
                pageText: 'Páginas: ',
                recordCountPageBoundTemplate: '{pageLowerBound} a {pageUpperBound} de',
                recordCountPageUnboundedTemplate: '{recordsShown} de',
                recordCountFilteredTemplate: ' (filtrado de {recordsTotal} registros en total)',
                recordCountText: 'Mostrando ',
                processingText: 'Procesando...'
            },
            params: {
                records: 'registros',
                queryRecordCount: 'total',
                totalRecordCount: 'total'
            },
        });
    }
});

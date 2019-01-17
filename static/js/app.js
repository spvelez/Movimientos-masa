$(document).foundation();
$(document).ready(function () {
    $('.delete-confirm').click(function () {
        if (confirm('¿Deseas eliminar este registro?')) {
            var form = document.createElement('form');
            form.action = this.href;
            form.method = 'post';
            $(form).appendTo('body');
            form.submit();
        }

        return false;
    });
});

// https://docs.djangoproject.com/zh-hans/2.2/ref/contrib/admin/javascript/#javascript-customizations-in-the-admin
(function($) {
    $(document).on('formset:added', function(event, $row, formsetName) {
        console.log(event)
        console.log($row)
        console.log(formsetName)
        if (formsetName == 'orderitem_set') {
            // Do something
        }
    });

    $(document).on('formset:removed', function(event, $row, formsetName) {
        // Row removed
        console.log(event)
        console.log($row)
        console.log(formsetName)
    });
})(django.jQuery);

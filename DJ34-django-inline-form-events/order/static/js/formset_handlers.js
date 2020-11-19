// https://docs.djangoproject.com/zh-hans/2.2/ref/contrib/admin/javascript/#javascript-customizations-in-the-admin
(function($) {



    var reinitDateTimeShortCuts = function() {
        // Reinitialize the calendar and clock widgets by force
        if (typeof DateTimeShortcuts !== "undefined") {
            $(".datetimeshortcuts").remove();
            DateTimeShortcuts.init();
        }
    };

    var updateSelectFilter = function() {
        // If any SelectFilter widgets are a part of the new form,
        // instantiate a new SelectFilter instance for it.
        if (typeof SelectFilter !== 'undefined') {
            $('.selectfilter').each(function(index, value) {
                var namearr = value.name.split('-');
                SelectFilter.init(value.id, namearr[namearr.length - 1], false);
            });
            $('.selectfilterstacked').each(function(index, value) {
                var namearr = value.name.split('-');
                SelectFilter.init(value.id, namearr[namearr.length - 1], true);
            });
        }
    };

    var initPrepopulatedFields = function(row) {
        row.find('.prepopulated_field').each(function() {
            var field = $(this),
                input = field.find('input, select, textarea'),
                dependency_list = input.data('dependency_list') || [],
                dependencies = [];
            $.each(dependency_list, function(i, field_name) {
                dependencies.push('#' + row.find('.field-' + field_name).find('input, select, textarea').attr('id'));
            });
            if (dependencies.length) {
                input.prepopulate(dependencies, input.attr('maxlength'));
            }
        });
    };


    $.fn.formsetAddInline = function(opts) {
        var options = $.extend({}, $.fn.formset.defaults, opts);
        var $this = $(this);
        var $parent = $this.parent();
        var updateElementIndex = function(el, prefix, ndx) {
            var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
            var replacement = prefix + "-" + ndx;
            if ($(el).prop("for")) {
                $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
            }
            if (el.id) {
                el.id = el.id.replace(id_regex, replacement);
            }
            if (el.name) {
                el.name = el.name.replace(id_regex, replacement);
            }
        };
        var totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
        var nextIndex = parseInt(totalForms.val(), 10);
        var maxForms = $("#id_" + options.prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");

        var showAddButton = maxForms.val() === '' || (maxForms.val() - totalForms.val()) > 0;
        if ($this.length && showAddButton) {
            var addButton = options.addButton;
            if (addButton === null) {
                if ($this.prop("tagName") === "TR") {
                    // If forms are laid out as table rows, insert the
                    // "add" button in a new table row:
                    var numCols = this.eq(-1).children().length;
                    // $parent.append('<tr class="' + options.addCssClass + '"><td colspan="' + numCols + '"><a href="#">' + options.addText + "</a></tr>");
                    addButton = $parent.find("tr:last a");
                } else {
                    // Otherwise, insert it immediately after the last form:
                    // 创建添加 inline 的按钮
                    // $this.filter(":last").after('<div class="' + options.addCssClass + '"><a href="#">' + options.addText + "</a></div>");
                    // 获取添加 inline 的按钮
                    addButton = $this.filter(":last").next().find("a");
                }
            }

            // 获取空的inline
            var template = $("#" + options.prefix + "-empty");
            // 拷贝template
            var row = template.clone(true);
            // 移除 empty-form 添加 dynamic-form
            row.removeClass(options.emptyCssClass)
            .addClass(options.formCssClass)
            .attr("id", options.prefix + "-" + nextIndex);
            if (row.is("tr")) {
                // If the forms are laid out in table rows, insert
                // the remove button into the last table cell:
                row.children(":last").append('<div><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></div>");
            } else if (row.is("ul") || row.is("ol")) {
                // If they're laid out as an ordered/unordered list,
                // insert an <li> after the last list item:
                row.append('<li><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></li>");
            } else {
                // Otherwise, just insert the remove button as the
                // last child element of the form's container:
                row.children(":first").append('<span><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></span>");
            }
            row.find("*").each(function() {
                updateElementIndex(this, options.prefix, totalForms.val());
            });
            // 添加到表单里
            // Insert the new form when it has been fully edited
            row.insertBefore($(template));

            // Update number of total forms
            $(totalForms).val(parseInt(totalForms.val(), 10) + 1);
            nextIndex += 1;
            // 达到最大值后隐藏添加按钮
            // Hide add button in case we've hit the max, except we want to add infinitely
            if ((maxForms.val() !== '') && (maxForms.val() - totalForms.val()) <= 0) {
                addButton.parent().hide();
            }
            // 添加删除事件
            // The delete button of each row triggers a bunch of other things
            row.find("a." + options.deleteCssClass).on('click', function(e1) {
                e1.preventDefault();
                // Remove the parent form containing this button:
                row.remove();
                nextIndex -= 1;
                // If a post-delete callback was provided, call it with the deleted form:
                if (options.removed) {
                    options.removed(row);
                }
                // 触发 formset:removed 事件
                $(document).trigger('formset:removed', [row, options.prefix]);
                // Update the TOTAL_FORMS form count.
                var forms = $("." + options.formCssClass);
                $("#id_" + options.prefix + "-TOTAL_FORMS").val(forms.length);
                // Show add button again once we drop below max
                if ((maxForms.val() === '') || (maxForms.val() - forms.length) > 0) {
                    addButton.parent().show();
                }
                // Also, update names and ids for all remaining form controls
                // so they remain in sequence:
                var i, formCount;
                var updateElementCallback = function() {
                    updateElementIndex(this, options.prefix, i);
                };
                for (i = 0, formCount = forms.length; i < formCount; i++) {
                    updateElementIndex($(forms).get(i), options.prefix, i);
                    $(forms.get(i)).find("*").each(updateElementCallback);
                }
            });
            // If a post-add callback was supplied, call it with the added form:
            if (options.added) {
                options.added(row);
            }
            // 触发 formset:added 事件
            $(document).trigger('formset:added', [row, options.prefix]);
        }
        return this
    }

    $(".js-inline-admin-formset").each(function() {
        var data = $(this).data(),
            inlineOptions = data.inlineFormset,
            selector;

        switch(data.inlineType) {
        case "stacked":
            selector = inlineOptions.name + "-group .inline-related";
            // $(selector).stackedFormset(selector, inlineOptions.options);
            break;
        case "tabular":
            console.log("tabular")
            selector = inlineOptions.name + "-group .tabular.inline-related tbody:first > tr";
            // $(selector).tabularFormset(selector, inlineOptions.options);

            var alternatingRows = function(row) {
                $(selector).not(".add-row").removeClass("row1 row2")
                .filter(":even").addClass("row1").end()
                .filter(":odd").addClass("row2");
            };

            var options = inlineOptions.options
            var opts= {
                prefix: options.prefix,
                addText: options.addText,
                formCssClass: "dynamic-" + options.prefix,
                deleteCssClass: "inline-deletelink",
                deleteText: options.deleteText,
                emptyCssClass: "empty-form",
                removed: alternatingRows,
                added: function(row) {
                    initPrepopulatedFields(row);
                    reinitDateTimeShortCuts();
                    updateSelectFilter();
                    alternatingRows(row);
                },
                addButton: options.addButton
            }

            // 自动添加两行inline
            $(this).formsetAddInline(opts)
            $(this).formsetAddInline(opts)
            break;
        }
    });

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

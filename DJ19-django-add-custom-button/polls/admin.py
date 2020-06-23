from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    change_form_template = 'admin/question/change_form.html'

    def response_change(self, request, obj):
        from django.http import HttpResponseRedirect
        if '_set-publish' in request.POST:
            obj.status = obj.PUBLISHED
            obj.save()
            self.message_user(request, '已发布')
            return HttpResponseRedirect('.')
        return super().response_change(request, obj)


admin.site.register(Question, QuestionAdmin)

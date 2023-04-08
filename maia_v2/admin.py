from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Questionnaire, QuestionCategory, Question,
    Respondant,
    QuestionnaireResponse, QuestionResponse,
)


class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'internal_name', 'questionnaire', 'questions')
    search_fields = ('name', 'internal_name')
    list_filter = ('questionnaire',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'category', 'questionnaire', 'reverse_score')
    search_fields = ('text',)
    list_filter = ('questionnaire', 'category')


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'internal_name', 'description', 'questions')
    search_fields = ('name', 'internal_name')


class QuestionnaireResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'questionnaire', 'respondant', 'date')
    search_fields = ('questionnaire', 'respondant')
    list_filter = ('questionnaire', 'respondant')
    readonly_fields = ('date', 'score', 'questionresponse_list')
    fieldsets = (
        (None, {
            'fields': ('questionnaire', 'respondant', 'date', 'score', 'questionresponse_list'),
        }),
    )

    def questionresponse_list(self, instance):
        question_responses = instance.questionresponse_set.all()
        return mark_safe('<p>{}</p>'.format(
            '<br>'.join(str(qr) for qr in question_responses)
        ))

admin.site.register(QuestionCategory, QuestionCategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Respondant)
admin.site.register(QuestionnaireResponse, QuestionnaireResponseAdmin)
admin.site.register(QuestionResponse)

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Questionnaire, QuestionCategory, Question,
    Respondant,
    QuestionnaireResponse, QuestionResponse,
)


class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'internal_name', 'questionnaire', 'questions')
    search_fields = ('name', 'internal_name')
    list_filter = ('questionnaire',)
    sortable_by = ('name', 'internal_name', 'questionnaire', 'questions')
    ordering = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'category', 'questionnaire', 'reverse_score')
    search_fields = ('text',)
    list_filter = ('questionnaire', 'category')
    sortable_by = ('id', 'text', 'category', 'questionnaire', 'reverse_score')
    ordering = ('id',)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'internal_name', 'description', 'questions')
    search_fields = ('name', 'internal_name')


class QuestionnaireResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'questionnaire', 'respondant', 'date', 'score')
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


class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'questionnaire', 'question', 'answer')
    search_fields = ('questionnaire_response', 'question')
    list_filter = ('questionnaire_response', 'question')
    sortable_by = ('id', 'questionnaire_response', 'question', 'answer')
    ordering = ('id',)

    def questionnaire(self, obj):
        return obj.question.questionnaire


class RespondantAdmin(admin.ModelAdmin):
    list_display = ('id', 'fingerprint', 'date', 'last_activity', 'questionnaire_responses')
    search_fields = ('fingerprint',)
    readonly_fields = ('last_activity', 'date')
    sortable_by = ('id', 'fingerprint', 'last_activity')
    ordering = ('id',)


admin.site.register(QuestionCategory, QuestionCategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Respondant, RespondantAdmin)
admin.site.register(QuestionnaireResponse, QuestionnaireResponseAdmin)
admin.site.register(QuestionResponse, QuestionResponseAdmin)

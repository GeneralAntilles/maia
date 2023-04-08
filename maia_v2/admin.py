from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Questionnaire, QuestionCategory, Question,
    Respondent,
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
    list_display = ('id', 'name', 'internal_name', 'description', 'question_list')
    search_fields = ('name', 'internal_name')
    readonly_fields = ('question_list',)
    fieldsets = (
        (None, {
            'fields': ('name', 'internal_name', 'description', 'instructions', 'question_list'),
        }),
    )

    def question_list(self, instance):
        questions = instance.question_set.all()
        return mark_safe('<table><thead><tr><th>Question</th><th>Answer</th></tr></thead><tbody>{}</tbody></table>'.format(
            '\n'.join('<tr><td>{}</td><td>{}</td></tr>'.format(
                question.id, question.text
            ) for question in questions
        )))

class QuestionnaireResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'questionnaire', 'respondent', 'date', 'score')
    search_fields = ('questionnaire', 'respondent')
    list_filter = ('questionnaire', 'respondent')
    readonly_fields = ('date', 'score', 'category_scores', 'questionresponse_list')
    fieldsets = (
        (None, {
            'fields': ('questionnaire', 'respondent', 'date', 'score', 'category_scores', 'questionresponse_list'),
        }),
    )

    def questionresponse_list(self, instance):
        question_responses = instance.questionresponse_set.all()
        return mark_safe('<table><thead><tr><th>Question</th><th>Answer</th></tr></thead><tbody>{}</tbody></table>'.format(
            '\n'.join('<tr><td>{}</td><td>{}</td></tr>'.format(
                question_response.question.text, question_response.answer
            ) for question_response in question_responses
        )))

    def category_scores(self, instance):
        score_dict = instance.score_dict
        return mark_safe('<table><thead><tr><th>Category</th><th>Score</th></tr></thead><tbody>{}</tbody></table>'.format(
            '\n'.join('<tr><td>{}</td><td>{:.02f}</td></tr>'.format(
                category, score
            ) for category, score in score_dict.items()
        )))


class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'questionnaire', 'question', 'answer')
    search_fields = ('questionnaire_response', 'question')
    list_filter = ('questionnaire_response', 'question')
    sortable_by = ('id', 'questionnaire_response', 'question', 'answer')
    ordering = ('id',)

    def questionnaire(self, obj):
        return obj.question.questionnaire


class RespondentAdmin(admin.ModelAdmin):
    list_display = ('id', 'fingerprint', 'date', 'last_activity', 'questionnaire_responses')
    search_fields = ('fingerprint',)
    readonly_fields = ('last_activity', 'date')
    sortable_by = ('id', 'fingerprint', 'last_activity')
    ordering = ('id',)


admin.site.register(QuestionCategory, QuestionCategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Respondent, RespondentAdmin)
admin.site.register(QuestionnaireResponse, QuestionnaireResponseAdmin)
admin.site.register(QuestionResponse, QuestionResponseAdmin)

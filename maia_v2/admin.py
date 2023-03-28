from django.contrib import admin

from .models import (
    Questionnaire, QuestionCategory, Question,
    User,
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


admin.site.register(QuestionCategory, QuestionCategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(User)
admin.site.register(QuestionnaireResponse)
admin.site.register(QuestionResponse)

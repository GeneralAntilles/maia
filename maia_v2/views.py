from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .forms import MAIAForm
from .models import Question, QuestionCategory, Questionnaire


def index(request):
    questionnaires = Questionnaire.objects.filter(published=True)

    return render(request, 'maia_v2/index.html', {'questionnaires': questionnaires})


class QuestionnaireFormView(View):
    def get(self, request, questionnaire):
        self.questionnaire = Questionnaire.objects.get(internal_name=questionnaire)
        response = {
            'questions': Question.objects.filter(questionnaire=self.questionnaire),
            'categories': QuestionCategory.objects.filter(questionnaire=self.questionnaire),
        }

        return render(request, f'maia_v2/{questionnaire}.html', response)

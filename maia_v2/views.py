from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .forms import get_questionnaire_form
from .models import Question, QuestionCategory, Questionnaire


def index(request):
    questionnaires = Questionnaire.objects.filter(published=True)

    return render(request, 'maia_v2/index.html', {'questionnaires': questionnaires})


class QuestionnaireFormView(View):
    def get(self, request, questionnaire):
        form = get_questionnaire_form(questionnaire)
        self.questionnaire = Questionnaire.objects.get(internal_name=questionnaire)
        response = {
            'questionnaire': self.questionnaire,
            'questions': Question.objects.filter(questionnaire=self.questionnaire),
            'categories': QuestionCategory.objects.filter(questionnaire=self.questionnaire),
            'form': form,
        }

        return render(request, f'maia_v2/{questionnaire}.html', response)

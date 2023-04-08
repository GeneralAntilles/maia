import hashlib
import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .forms import get_questionnaire_form
from .models import (Question, QuestionCategory, QuestionResponse,
                     Questionnaire, QuestionnaireResponse,
                     Respondent)


def index(request):
    questionnaires = Questionnaire.objects.filter(published=True)

    return render(request, 'maia_v2/index.html', {'questionnaires': questionnaires})


class QuestionnaireFormView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.questionnaire = None
        self.questions = None
        self.categories = None
        self.form = None

    def get(self, request, questionnaire):
        self.form = get_questionnaire_form(questionnaire)
        self.get_questionnaire_data(questionnaire)

        response = {
            'questionnaire': self.questionnaire,
            'questions': self.questions,
            'categories': self.categories,
            'form': self.form,
        }

        return render(request, f'maia_v2/{questionnaire}.html', response)

    def post(self, request, questionnaire):
        self.form = get_questionnaire_form(questionnaire)
        self.get_questionnaire_data(questionnaire)

        form_submission = self.form(request.POST)
        response = {
            'questionnaire': self.questionnaire,
            'questions': self.questions,
            'categories': self.categories,
            'form': self.form,
        }

        if form_submission.is_valid():
            fingerprint_raw = ''.join([
                request.META.get('HTTP_USER_AGENT', ''),
                request.META.get('HTTP_ACCEPT_ENCODING', ''),
                request.META.get('REMOTE_ADDR', ''),
            ])
            request.fingerprint = hashlib.md5(
                fingerprint_raw.encode('utf-8')).hexdigest()
            # Get a user or create one
            try:
                respondent = Respondent.objects.get(fingerprint=request.fingerprint)
            except Respondent.DoesNotExist:
                respondent = Respondent(
                    fingerprint=request.fingerprint,
                )

            # The object for the form submission
            questionnaire_response = QuestionnaireResponse(
                questionnaire=self.questionnaire,
                respondent=respondent,
            )

            # Collecting the question responses
            question_responses = {}
            for question in self.questions:
                question_submission = form_submission.cleaned_data[str(question.id)]
                question_responses[question.id] = QuestionResponse(
                    questionnaire_response=questionnaire_response,
                    question=question,
                    answer=question_submission,
                )

            # Saving the questionnaire response and question responses
            respondent.save()
            questionnaire_response.save()
            for question_response in question_responses.values():
                question_response.save()

            return HttpResponseRedirect(f'/questionnaire/{questionnaire}/')
        else:
            return render(request, f'maia_v2/{questionnaire}.html', response)

    def get_questionnaire_data(self, questionnaire):
        self.questionnaire = Questionnaire.objects.get(internal_name=questionnaire)
        self.questions = Question.objects.filter(questionnaire=self.questionnaire)
        self.categories = QuestionCategory.objects.filter(questionnaire=self.questionnaire)

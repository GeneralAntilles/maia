import hashlib
import json
import uuid

import numpy as np

from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import get_questionnaire_form
from .models import (Question, QuestionCategory, QuestionResponse,
                     Questionnaire, QuestionnaireResponse,
                     Respondent, QuestionnaireData)


def index(request):
    questionnaires = Questionnaire.objects.filter(published=True)

    return render(
        request,
        'maia_v2/index.html',
        {
            'questionnaires': questionnaires,
            'current_site': Site.objects.get_current(),
        },
    )


class AboutView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_site = Site.objects.get_current()

    def get(self, request):
        return render(
            request, 'maia_v2/about.html',
            {'current_site': self.current_site},
        )


class QuestionnaireFormView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_site = Site.objects.get_current()
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
            'current_site': self.current_site,
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
            'current_site': self.current_site,
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

            return HttpResponseRedirect(f'/questionnaire/{questionnaire}/results/{respondent.fingerprint}/')
        else:
            return render(request, f'maia_v2/{questionnaire}.html', response)

    def get_questionnaire_data(self, questionnaire):
        self.questionnaire = Questionnaire.objects.get(internal_name=questionnaire)
        self.questions = Question.objects.filter(questionnaire=self.questionnaire)
        self.categories = QuestionCategory.objects.filter(questionnaire=self.questionnaire)


class QuestionnaireResultsView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_site = Site.objects.get_current()

    def get(self, request, questionnaire, respondent):
        questionnaire = Questionnaire.objects.get(internal_name=questionnaire)
        questionnaire_data = QuestionnaireData.objects.filter(questionnaire=questionnaire)
        respondent = Respondent.objects.get(fingerprint=respondent)
        respondents = QuestionnaireResponse.objects.filter(questionnaire=questionnaire).count()
        questionnaire_response = QuestionnaireResponse.objects.filter(
            respondent=respondent).latest('date')

        question_responses = questionnaire_response.questionresponse_set.all()

        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        percentile = ordinal(int(questionnaire_response.percentile))
        # Calibrate the number of bin steps based on the total number of
        # respondents. No point showing a lot of histogram bins if there are
        # only a few respondents.
        if respondents > 20:
            bin_step = 3
        elif respondents > 50:
            bin_step = 1
        else:
            bin_step = 10
        bucket = self.histogram_bucket(questionnaire_response.score,
                                       questionnaire, bin_step=bin_step)
        return render(
            request,
            'maia_v2/results.html',
            {
                'questionnaire': questionnaire,
                'papers': questionnaire_data,
                'respondent': respondent,
                'respondents': respondents,
                'question_responses': question_responses,
                'results': questionnaire_response,
                'scores': json.dumps(questionnaire_response.score_dict),
                'total_score': questionnaire_response.score,
                'score_percentile': percentile,
                'bucket': bucket,
                'current_site': self.current_site,
            },
        )

    def histogram_bucket(self, data, questionnaire, bin_step=1):
        """
        Determine the value of the histogram bin the given data point falls into.
        """
        bins = np.array(
            range(questionnaire.scale_min * 10,
                  questionnaire.scale_max * 10 + 1, bin_step)
        ) / 10
        return bins[np.digitize(data, bins) - 1]


class APIQuestionnaireResultsView(APIView):
    def get(self, request, questionnaire, respondent):
        questionnaire = Questionnaire.objects.get(internal_name=questionnaire)
        respondent = Respondent.objects.get(fingerprint=respondent)
        questionnaire_response = QuestionnaireResponse.objects.filter(
            respondent=respondent).latest('date')
        scores = []
        for key, value in questionnaire_response.score_dict.items():
            scores.append({'name': key, 'value': value})
        return Response(scores)


class APIQuestionnaireComparisonView(APIView):
    def get(self, request, questionnaire, respondent):
        questionnaire = Questionnaire.objects.get(internal_name=questionnaire)
        categories = QuestionCategory.objects.filter(questionnaire=questionnaire).values('internal_name', 'name')

        # Generate comparison data from the database
        comparison_data_sources = QuestionnaireData.objects.filter(questionnaire=questionnaire)
        comparison_data = []
        for comparison_data_source in comparison_data_sources:
            comparison_data.append({
                'name': comparison_data_source.name,
                'description': comparison_data_source.description,
                'scores': json.loads(comparison_data_source.scores),
                'total_score': comparison_data_source.score,
            })

        # Generate comparison data from the respondents
        questionnaire_responses = QuestionnaireResponse.objects.filter(questionnaire=questionnaire)
        respondents_summary_data = self.construct_respondents_summary_data(questionnaire_responses, categories)

        # Reshape to feed the Charts.js bar chart
        category_map = {c['internal_name']: c['name'] for c in categories}
        # Generate the data from each comparison data source dynamically
        # for each category
        comparison_dict = {}
        for comparison_data_source in comparison_data:
            # Each comparison data source should have a dict with the scores
            # for each category { 'name': 'category_name', 'score': 0.5 }
            scores = []
            for category in category_map.keys():
                scores.append({
                    'name': category_map[category],
                    'value': comparison_data_source['scores'][category]
                })
            comparison_dict[comparison_data_source['name']] = scores

        return Response(comparison_dict)

    def construct_respondents_summary_data(self, questionnaire_responses, categories):
        """
        Construct a summary of the respondents' scores to match the
        comparison_data available in the database.
        """
        scores = {}
        for category in categories:
            scores[category['name']] = []
        for questionnaire_response in questionnaire_responses:
            for category in categories:
                scores[category['name']].append(
                    questionnaire_response.score_dict[category['name']])

        return scores


class APIQuestionnaireStatsView(APIView):
    def get(self, request, questionnaire, respondent):
        questionnaire = Questionnaire.objects.get(internal_name=questionnaire)
        respondent = Respondent.objects.get(fingerprint=respondent)
        questionnaire_response = QuestionnaireResponse.objects.filter(
            respondent=respondent).latest('date')
        responses = QuestionnaireResponse.objects.all().filter(questionnaire=questionnaire)

        scores = [response.score for response in responses]

        # Calibrate the number of bin steps based on the total number of
        # respondents. No point showing a lot of histogram bins if there are
        # only a few respondents.
        if responses.count() > 20:
            bin_step = 3
        elif responses.count() > 50:
            bin_step = 1
        else:
            bin_step = 10
        histogram_data = self.histogram_data(scores, questionnaire,
                                             bin_step=bin_step)

        return Response(histogram_data)

    def histogram_data(self, data, questionnaire, bin_step=1):
        # Construct the histogram data
        bins = np.array(
            range(questionnaire.scale_min * 10,
                  questionnaire.scale_max * 10 + 1, bin_step)
        ) / 10
        x_axis: list = []
        for i in bins:
            x_axis.append(i)
        histogram_data = {'data1': x_axis}

        # Bin the scores into buckets with numpy
        buckets = np.histogram(data, bins=bins)[0]

        y_axis = []
        for bucket in buckets:
            y_axis.append(bucket)
        histogram_data['Respondents'] = y_axis

        return histogram_data

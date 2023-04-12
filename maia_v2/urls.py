from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'questionnaire/<str:questionnaire>/',
        views.QuestionnaireFormView.as_view(),
        name='questionnaire',
    ),
    path(
        'questionnaire/<str:questionnaire>/submit/',
        views.QuestionnaireFormView.as_view(),
        name='questionnaire-submit',
    ),
    path(
        'questionnaire/<str:questionnaire>/results/<str:respondent>/',
        views.QuestionnaireResultsView.as_view(),
        name='questionnaire-results',
    ),
    path(
        'questionnaire/<str:questionnaire>/results/<str:respondent>/scores/',
        views.APIQuestionnaireResultsView.as_view(),
        name='questionnaire-results-api',
    ),
    path(
        'questionnaire/<str:questionnaire>/results/<str:respondent>/stats/',
        views.APIQuestionnaireStatsView.as_view(),
        name='questionnaire-stats',
    ),
]
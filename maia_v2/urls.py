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
]
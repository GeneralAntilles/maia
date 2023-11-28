from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
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
        'questionnaire/<str:questionnaire>/results/<str:respondent>/comparison/',
        views.APIQuestionnaireComparisonView.as_view(),
        name='questionnaire-comparison',
    ),
    path(
        'questionnaire/<str:questionnaire>/results/<str:respondent>/stats/',
        views.APIQuestionnaireStatsView.as_view(),
        name='questionnaire-stats',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

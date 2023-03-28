from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'questionnaire/<str:questionnaire>/',
        views.QuestionnaireFormView.as_view(),
        name='questionnaire',
    ),
]
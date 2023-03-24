from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MAIAForm
from .models import Question, QuestionCategory


def index(request):
    form = MAIAForm()
    print(form)
    return render(
        request, 'maia_v2/index.html',
        {'questions': Question.objects.all(), 'categories': QuestionCategory.objects.all()},
    )


def questionnaire(request):
    if request.method == 'POST':
        form = MAIAForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        form = MAIAForm()
    return render(request, 'maia_v2/questionnaire.html', {'form': form})
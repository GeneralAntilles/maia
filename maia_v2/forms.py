import textwrap
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Fieldset, Layout, Submit

from .models import Question, QuestionCategory, QuestionnaireResponse


def get_questionnaire_form(questionnaire):
    """
    Dynamically returns the correct questionnaire form for the given questionnaire.

    Args:
        questionnaire (str): The internal name of the questionnaire.

    Returns:
        ModelForm subclass: The questionnaire form.
    """
    if questionnaire == 'maia_v2':
        return MAIAForm

class MAIAForm(forms.ModelForm):
    """
    Form for the MAIA v2 questionnaire.

    This form is dynamically generated from the questions in the database.
    """
    class Meta:
        model = QuestionnaireResponse
        fields = []

    radio_choices = {
        False: ((0, ''), (1, ''), (2, ''), (3, ''), (4, ''), (5, '')),
        True: ((5, ''), (4, ''), (3, ''), (2, ''), (1, ''), (0, ''))
    }

    for question in Question.objects.all():
        locals()[str(question.id)] = forms.IntegerField(
            label=f'{question.id}. {question.text}',
            min_value=0, max_value=5,
            required=question.required,
            widget=forms.RadioSelect(
                choices=radio_choices[question.reverse_score]),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_id = 'maia-v2'
        self.helper.form_method = 'post'
        self.helper.form_action = (
            f'/questionnaire/maia_v2/submit/')
        self.helper.wrapper_class = 'form-group'

        self.helper.layout = Layout()

        questionnaire_layout = Layout()
        for category in QuestionCategory.objects.all():
            category_layout = Layout(Fieldset(
                category.name,
                template='maia_v2/custom_fieldset.html',
                css_class=category.internal_name,
            ))
            for question in category.question_set.all():
                category_layout[0].append(str(question.id))
            questionnaire_layout.append(category_layout)

        self.helper.layout.append(questionnaire_layout)
        self.helper.layout.append(HTML(
            '<p><i>Submit your questionnaire to see how your score compares!</i></p>'))
        self.helper.add_input(Submit('submit', 'Submit'))

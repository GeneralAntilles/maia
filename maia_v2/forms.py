from django import forms

from .models import Question


class MAIAForm(forms.ModelForm):
    """
    Form for the MAIA v2 questionnaire.

    This form is dynamically generated from the questions in the database.
    """
    class Meta:
        model = Question
        fields = ['id', 'text', 'category', 'reverse_score']

    template_name = 'maia_v2/questionnaire.html'
    radio_choices = {
        False: ((0, ''), (1, ''), (2, ''), (3, ''), (4, ''), (5, '')),
        True: ((5, ''), (4, ''), (3, ''), (2, ''), (1, ''), (0, ''))
    }

    id = forms.IntegerField(widget=forms.HiddenInput())
    text = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    reverse_score = forms.BooleanField(widget=forms.HiddenInput())

    score = forms.IntegerField(
        label="",
        min_value=0,
        max_value=5,
        required=True,
        widget=forms.RadioSelect(),
    )

    def __init__(self, *args, **kwargs):
        super(MAIAForm, self).__init__(*args, **kwargs)
        self.fields['score'].widget.choices = self.radio_choices[
            self.instance.reverse_score]


    # for question in Question.objects.all():
    #     locals()[question.id] = forms.IntegerField(
    #         label=question.text,
    #         min_value=0, max_value=5,
    #         required=True,
    #         widget=forms.RadioSelect(
    #             choices=radio_choices[question.reverse_score]),
    #     )

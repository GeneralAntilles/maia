import numpy as np

from django.db import models
from meta.models import ModelMeta



class Questionnaire(ModelMeta, models.Model):
    """
    Model for the questionnaires.
    """
    # Questionnaires have a presentation name and an internal name
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    # If short_name is empty use name instead
    short_name = models.CharField(max_length=30, null=True, blank=True)
    internal_name = models.CharField(max_length=100, unique=True, null=False,
                                     blank=False)
    source = models.URLField(null=True, blank=True)
    published = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    scale = models.CharField(max_length=100, null=True, blank=True)
    scale_min = models.IntegerField(null=True, blank=True)
    scale_max = models.IntegerField(null=True, blank=True)

    preview_image = models.ImageField(upload_to='questionnaire_images',
                                      null=True, blank=True)

    _metadata = {
        'title': 'Abelify',
        'description': 'get_meta_description',
        'keywords': ['Python', 'Django', 'open source', 'questionnaire'],
        'image': 'get_meta_image',
        'use_sites': True,
        'og_type': 'website',
        'use_og': True,
        'use_twitter': True,
    }

    @property
    def display_name(self):
        return self.short_name or self.name

    @property
    def questions(self):
        return self.question_set.count()

    def get_meta_image(self):
        return self.preview_image.url if self.preview_image else 'media/630.png'

    def get_meta_description(self):
        return self.description

    def __str__(self):
        return str(self.internal_name)


class QuestionnaireData(models.Model):
    """
    Model for data from other papers that can be used for comparison.

    We do not have access to the raw data so this is just high-level results
    data.
    """
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE,
                                      null=False, blank=False, default=1)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    internal_name = models.CharField(max_length=100, unique=True, null=False,
                                     blank=False)
    paper_name = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    source = models.URLField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    scores = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.internal_name)

class QuestionCategory(models.Model):
    """
    Model for the question categories.
    """
    class Meta:
        verbose_name_plural = 'Question categories'

    # Categories have a presentation name and an internal name
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    internal_name = models.CharField(max_length=100, unique=True, null=False,
                                     blank=False)

    # Questionnaire is a foreign key to the Questionnaire model
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE,
                                      null=False, blank=False, default=1)

    @property
    def questions(self):
        return self.question_set.count()

    def __str__(self):
        return self.internal_name


class Question(models.Model):
    """
    Model for the questions.
    """
    text = models.CharField(max_length=2000)
    # Question IDs are provided by the test creator
    id = models.IntegerField(primary_key=True, unique=True, null=False,
                             blank=False)
    # QuestionCategory is a foreign key to the QuestionCategory model
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE,
                                 null=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE,
                                      null=False, blank=False, default=1)
    required = models.BooleanField(default=True)
    reverse_score = models.BooleanField(default=False)


    def __str__(self):
        if self.category is None:
            return f'{self.id} {self.text}'

        return f'{self.id} {self.text} ({self.category.name})'


class Respondent(models.Model):
    """
    Model for site users. Users are created when they take a test and are
    associated with the test results. We try to fingerprint each user by their
    IP address and browser fingerprint, but won't retain any personally
    identifiable information or IP addresses.
    """
    # We store an MD5 hash of the user's IP address and browser fingerprint,
    # but we don't store the IP address or fingerprint itself
    fingerprint = models.CharField(max_length=32, unique=True, null=False,
                                   blank=False)

    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    @property
    def last_activity(self):
        """
        Return the last activity time for the user.
        """
        return self.questionnaireresponse_set.latest('date').date

    @property
    def questionnaire_responses(self):
        """
        Return the number of questionnaire responses for the user.
        """
        return self.questionnaireresponse_set.all().count()

    def __str__(self):
        return f'{self.id} ({self.fingerprint})'


class QuestionnaireResponse(models.Model):
    """
    Model for questionnaire responses.
    """
    # Questionnaire is a foreign key to the Questionnaire model
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE,
                                      null=False, blank=False)
    # User is a foreign key to the User model
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE,
                                   null=False, blank=False)
    # We store the date and time the questionnaire was completed
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    score = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate the score.
        """
        super().save(*args, **kwargs)
        if (
            self.score is None and
            self.questionnaire.questions == self.questionresponse_set.count()
        ):
            self.score = self.calculate_score()
            super().save(*args, **kwargs)

    def calculate_score(self):
        """
        Calculate the score for the questionnaire response.
        """
        if self.questionnaire.questions > self.questionresponse_set.count():
            return None

        score = 0
        for category in self.questionnaire.questioncategory_set.all():
            category_score = 0
            for question_response in self.questionresponse_set.filter(
                    question__category=category):
                category_score += question_response.answer

            category_score = category_score / category.questions
            score += category_score

        score = round(score / self.questionnaire.questioncategory_set.count(), 2)
        return score

    @property
    def percentile(self):
        """
        Calculate the percentile for the questionnaire response.
        """
        score = self.score
        questionnaire_responses = QuestionnaireResponse.objects.filter(
            questionnaire=self.questionnaire)
        scores = sorted([qr.score for qr in questionnaire_responses])
        return np.sum(np.array(scores) <= score) / len(scores) * 100

    @property
    def score_dict(self):
        """
        Calculate the score for the questionnaire response.
        """
        score = {}
        for category in self.questionnaire.questioncategory_set.all():
            category_score = 0
            for question_response in self.questionresponse_set.filter(
                    question__category=category):
                category_score += question_response.answer

            category_score = category_score / category.questions
            score[category.name] = category_score

        return score

    @property
    def percentile_dict(self):
        """
        Calculate the percentile for each category score in the questionnaire
        response.
        """
        score = {}
        for category in self.questionnaire.questioncategory_set.all():
            category_score = 0
            for question_response in self.questionresponse_set.filter(
                    question__category=category):
                category_score += question_response.answer

            category_score = category_score / category.questions
            questionnaire_responses = QuestionnaireResponse.objects.filter(
                questionnaire=self.questionnaire)
            scores = sorted([qr.score for qr in questionnaire_responses])
            score[category.name] = np.sum(np.array(scores) <= category_score) / len(scores) * 100

        return score

    def __str__(self):
        return f'{self.questionnaire.name} ({self.respondent.id}) {self.date.date()} - {self.score}'


class QuestionResponse(models.Model):
    """
    Model for question responses.
    """
    # QuestionnaireResponse is a foreign key to the QuestionnaireResponse
    # model
    questionnaire_response = models.ForeignKey(QuestionnaireResponse,
                                               on_delete=models.CASCADE,
                                               null=False, blank=False)
    # Question is a foreign key to the Question model
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 null=False, blank=False)
    answer = models.IntegerField(null=False, blank=False)

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate the score for the questionnaire
        response.
        """
        super().save(*args, **kwargs)
        self.questionnaire_response.score = self.questionnaire_response.calculate_score()
        self.questionnaire_response.save()

    def __str__(self):
        return f'{self.question.id}. {self.question.text}: {self.answer}'

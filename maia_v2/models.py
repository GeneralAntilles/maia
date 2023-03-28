from django.db import models


class Questionnaire(models.Model):
    """
    Model for the questionnaires.
    """
    # Questionnaires have a presentation name and an internal name
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    internal_name = models.CharField(max_length=100, unique=True, null=False,
                                     blank=False)
    source = models.URLField(null=True, blank=True)
    published = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)

    @property
    def questions(self):
        return self.question_set.count()

    def __str__(self):
        return self.internal_name


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
    reverse_score = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.text} ({self.category.name})'


class User(models.Model):
    """
    Model for site users. Users are created when they take a test and are
    associated with the test results. We try to fingerprint each user by their
    IP address and browser fingerprint, but won't retain any personally
    identifiable information or IP addresses.
    """
    # We use a UUID to identify users, but we don't want to expose this to
    # users, so we use a random string instead
    id = models.CharField(max_length=100, primary_key=True, unique=True,
                          null=False, blank=False)
    # We store a hash of the user's IP address and browser fingerprint, but
    # we don't store the IP address or fingerprint itself
    fingerprint = models.CharField(max_length=254, unique=True, null=False,
                                   blank=False)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
                             blank=False)
    # We store the date and time the questionnaire was completed
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return f'{self.questionnaire.name} ({self.user.id})'


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

    def __str__(self):
        return f'{self.question.text} ({self.question.id})'

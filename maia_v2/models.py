from django.db import models


class QuestionCategory(models.Model):
    """
    Model for the question categories.

    Categories are provided by the MAIA test creators.
    """
    # Categories have a presentation name and an internal name
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    internal_name = models.CharField(max_length=100, unique=True, null=False,
                                     blank=False)

    def __str__(self):
        return f'{self.name} ({self.internal_name})'


class Question(models.Model):
    """
    Model for the questions.

    Questions are provided by the MAIA test creators.
    """
    text = models.CharField(max_length=2000)
    # Question IDs are provided by the test creator
    id = models.IntegerField(primary_key=True, unique=True, null=False,
                             blank=False)
    # QuestionCategory is a foreign key to the QuestionCategory model
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL,
                                 null=True)
    reverse_score = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.id}: {self.text} ({self.category.name})'

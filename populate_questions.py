import os
import django
from maia.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maia.settings")

django.setup()

from maia_v2.models import Question
from maia_v2.models import QuestionCategory
from questions import questions


def populate_questions():
    # Category is a foreign key to QuestionCategory
    question_objects = [
        Question(text=q['question'], id=i + 1,
                 category=QuestionCategory.objects.get(internal_name=q['category']),
                 reverse_score=q['reverse']) for i, q in enumerate(questions)
    ]

    Question.objects.bulk_create(question_objects)

populate_questions()

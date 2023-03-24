import os
import django
from maia.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maia.settings")

django.setup()

from maia_v2.models import QuestionCategory

categories = {
    'noticing': 'Noticing',
    'not-distracting': 'Not-Distracting',
    'not-worrying': 'Not-Worrying',
    'attention_regulation': 'Attention Regulation',
    'emotional_awareness': 'Emotional Awareness',
    'self-regulation': 'Self-Regulation',
    'body_listening': 'Body Listening',
    'trusting': 'Trusting',
}


def populate_categories():
    category_objects = [
        QuestionCategory(name=value, internal_name=key) for key, value in categories.items()
    ]

    QuestionCategory.objects.bulk_create(category_objects)

populate_categories()

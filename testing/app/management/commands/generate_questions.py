from django.core.management.base import BaseCommand
from app.models import TestSet, Question, Answer
import random

class Command(BaseCommand):
    help = 'Create menu items for the application'

    def handle(self, *args, **kwargs):
        # Создание меню
        for i in range(10):

            test_set, created = TestSet.objects.get_or_create(name=f'Test set #{i}')

            for j in range(random.randint(7,12)):
                
                question, created = Question.objects.get_or_create(
                    test_set=test_set, 
                    text=f'[Test set #{i}] Question #{j}')

                for k in range(random.randint(2,6)):

                    is_correct = True if k == 0 else random.randint(1,10) == 5
                    answer, created = Answer.objects.get_or_create(
                        question=question,
                        text=f'[Test set #{i} Question #{i}] Answer #{k} ({is_correct})',
                        is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS('Successfully created test sets'))
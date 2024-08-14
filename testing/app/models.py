from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TestSet(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Question(models.Model):
    test_set = models.ForeignKey(TestSet, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text
    
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_set = models.ForeignKey(TestSet, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

class UserAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, related_name='user_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ManyToManyField(Answer)
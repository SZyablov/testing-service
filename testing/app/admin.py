from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import TestSet, Question, Answer
from django.forms.models import BaseInlineFormSet

class AnswerInlineFormSet(BaseInlineFormSet):

    # validation function
    def clean(self):

        super().clean()

        if any(self.errors):
            return
        
        correct_answers = 0

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if form.cleaned_data.get('is_correct', False):
                correct_answers += 1

        if correct_answers == 0:
            raise ValidationError('Каждый вопрос должен иметь хотя бы один правильный ответ')
        if correct_answers == len(self.forms) - 1:
            raise ValidationError('Все ответы не могут быть правильными')

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    formset = AnswerInlineFormSet

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class TestSetAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(TestSet, TestSetAdmin)
admin.site.register(Question, QuestionAdmin)
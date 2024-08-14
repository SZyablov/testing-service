from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Answer, UserAnswer

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['answer']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        answers = Answer.objects.filter(question=question)
        correct_answers_count = answers.filter(is_correct=True).count()

        # if there is 1 correct answer - create radio button form
        if correct_answers_count == 1:
            self.fields['answer'] = forms.ModelChoiceField(
                queryset=answers,
                widget=forms.RadioSelect,
                empty_label=None,
                label='Выберите правильный ответ:'
            )
        # else we will create a couple of checkboxes
        else:
            self.fields['answer'] = forms.ModelMultipleChoiceField(
                queryset=answers,
                widget=forms.CheckboxSelectMultiple,
                label='Выберите правильные ответы:'
            )
    
    def clean_answer(self):
        data = self.cleaned_data['answer']
        if not data:
            raise forms.ValidationError('Необходимо выбрать хотя бы один ответ.')
        return data

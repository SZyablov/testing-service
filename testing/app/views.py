from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TestSet, UserTest, Question, UserAnswer, Answer
from .forms import LoginForm, SignUpForm, AnswerForm

#
# Main page with the list of tests
# index
@login_required
def index(request):
    tests = TestSet.objects.all()
    return render(request, 'index.html', {'tests': tests})

# Function to get the next question
def get_next_question(test_set, user_test):
    next_question = Question.objects.filter(test_set=test_set).exclude(
        id__in=user_test.user_answers.values_list('question_id', flat=True)
    ).first()
    return next_question

#
# Endpoint for taking test
# It gives either unanswered question or test result
# test/<int:test_id>/
@login_required
def take_test(request, test_id):
    test_set = get_object_or_404(TestSet, id=test_id)
    user_test, created = UserTest.objects.get_or_create(user=request.user, test_set=test_set)

    # if user answered question
    if request.method == 'POST':
        # here we get that question
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        form = AnswerForm(request.POST, question=question)
        if form.is_valid():

            # here we get the user answer (or create if it does not exist)
            user_answer, created = UserAnswer.objects.get_or_create(user_test=user_test, question=question)
            # if the answer was already in db
            if not created:
                # we just move forward without saving new answer
                next_question = get_next_question(test_set, user_test)
                if next_question:
                    return redirect('question', test_id=test_set.id, question_id=next_question.id, redirected=True)
                else:
                    return redirect('result', user_test_id=user_test.id)
                
            # or if the answer wasn't in database, here we will save it...
            if isinstance(form.cleaned_data['answer'], Answer):
                user_answer.answer.set([form.cleaned_data['answer'].id])
            else:
                user_answer.answer.set([answer.id for answer in list(form.cleaned_data['answer'])])
            user_answer.save()

            # ...and move to the next question (or to the result)
            next_question = get_next_question(test_set, user_test)
            if next_question:
                return redirect('question', test_id=test_set.id, question_id=next_question.id, redirected=True)
            else:
                return redirect('result', user_test_id=user_test.id)
    
    # if the user just selected a test, we will give them the first unanswered question
    else:
        next_question = get_next_question(test_set, user_test)
        if next_question:
            return redirect('question', test_id=test_set.id, question_id=next_question.id, redirected=True)
        else:
            return redirect('result', user_test_id=user_test.id)

#
# Page with the question
# test/<int:test_id>/question/<int:question_id>/
@login_required
def question(request, test_id, question_id, redirected = False):
    if not redirected:
        test_set = get_object_or_404(TestSet, id=test_id)
        user_test, created = UserTest.objects.get_or_create(user=request.user, test_set=test_set)
        question = get_next_question(test_set, user_test)
        if question:
            return redirect('question', test_id=test_set.id, question_id=question.id)
        else:
            return redirect('result', user_test_id=user_test.id)

    question = get_object_or_404(Question, id=question_id)
    form = AnswerForm(question=question)
    return render(request, 'question.html', {
        'question': question,
        'test_id': {
            'id': test_id
        },
        'form': form})

#
# Page with the result if the test was completed
# result/<int:user_test_id>/
@login_required
def result(request, user_test_id):
    user_test = get_object_or_404(UserTest, id=user_test_id)
    correct_answers = sum(
        1 for user_answer in user_test.user_answers.all() 
        if all(answer.is_correct for answer in user_answer.answer.all())
        and user_answer.answer.count() == user_answer.question.answers.filter(is_correct=True).count()
    )
    total_questions = user_test.user_answers.count()
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    return render(request, 'result.html', {
        'user_test': user_test,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'score': round(score, 2)
    })

#
# Sign-up page
def user_sign_up(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.info(request, 'You have been successfully signed up. You can log-in with your fresh account')
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'sign_up.html', {'form': form})

#
# Login page
def user_login(request):

    redirecting_to = 'index'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(redirecting_to)
                else:
                    messages.error(request, 'This account is disabled')
                    return render(request,'login.html',{'form': form})
            else:
                messages.error(request, 'Invalid username or password')
                return render(request,'login.html',{'form': form})
    else:
        form = LoginForm()

    if request.user.is_authenticated:
        return redirect(redirecting_to)
    
    return render(request, 'login.html', {'form': form})

#
# Logout endpoint, will redirect to login page
def user_logout(request):

    logout(request)
    messages.info(request, 'You have been successfully logged out. You can log-in again')

    return redirect('login')
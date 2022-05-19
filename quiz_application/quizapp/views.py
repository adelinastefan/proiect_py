from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import Questions

def homepage(request):
    if request.method == 'POST':
        print(request.POST)
        questions = Questions.objects.all()
        score = 0
        false = 0
        true = 0
        total = 0
        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.answer == request.POST.get(q.question):
                score += 10
                true += 1
            else:
                false += 1
        context = {
            'score': score,
            'true': true,
            'false': false,
            'total': total
        }
        return render(request, 'quiz/resultpage.html', context)
    else:
        questions = Questions.objects.all()
        context = {
            'questions': questions
        }
        return render(request, 'quiz/hompage.html', context)


def add_question(request):
    if request.user.is_staff:
        form = add_questionform()
        if (request.method == 'POST'):
            form = add_questionform(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('/')
        context = {'form': form}
        return render(request, 'quiz/add_question.html', context)
    else:
        return redirect('homepage')


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('loginpage')
        context = {
            'form': form,
        }
        return render(request, 'quiz/registerpage.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'quiz/loginpage.html', context)


def logoutpage(request):
    logout(request)
    return redirect('/')
import random

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import format_html

from .forms import *
from .models import QuizQuestion, Category, Contact, FAQ

# Create your views here.

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been submitted successfully!')
            return redirect(request.path) #Redirect to the same page
    else:
        form = ContactForm()
    return form

def home(request):
    form = contact_view(request)
    context = {
        'form': form,
    }
    return render(request, 'index.html', context)

def about_view(request):
    form = contact_view(request)
    context = {
        'form': form,
    }
    return render(request, 'about.html', context)

def quiz_view(request):
    questions = list(QuizQuestion.objects.all())
    if not questions:
        raise Http404("No questions available")
    question = random.choice(questions)
    
    if 'skip' in request.POST:
        message = f"You skipped the previous question. A new question has been generated."
        return redirect('quiz_view')
    context = {
        'question': question,
    }
    return render(request, 'quiz/quiz.html', context)

def quiz_result_view(request, question_id):
    question = get_object_or_404(QuizQuestion, pk=question_id)
    user_answer = request.POST.get('option')
    is_correct = user_answer == question.correct_option
    context = {
        'question': question,
        'user_answer': user_answer,
        'is_correct': is_correct,
    }
    return render(request, 'quiz/result.html', context)

def take_quiz_(request):
    questions = list(QuizQuestion.objects.all())
    if not questions:
        raise Http404("No questions available")
    
    question = random.choice(questions)
    print(question)
    
    request.session['score'] = request.session.get('score', 0)
    request.session['attempts'] = request.session.get('attempts', 0)
    
    if 'skip' in request.POST:
        message = f"You skipped the previous question. A new question has been generated."
        messages.info(request, message)
        request.session['attempts'] += 1
        return redirect('take_quiz_')
    
    if request.method == 'POST':
        print(question)
        user_answer = request.POST.get('option')
        print(question, user_answer)
        
        if user_answer == question.correct_option:
            message = "Correct! Well done."
            messages.success(request, message)
            request.session['score'] += 10
            request.session['attempts'] += 1
            return redirect('take_quiz_')
        else:
            message = f"Sorry, that's not correct"
            messages.warning(request, message)
            request.session['score'] -= 5
            request.session['attempts'] += 1
            return redirect('take_quiz_')
        
        """
        print('Done', request.session['score'], request.session['attempts'])
        context = {
            'attempts': request.session['attempts'],
            'score': request.session['score'],
        }
        return render(request, 'quiz/take_quiz.html', context)
        """
    context = {
        'question': question,
        'attempts': request.session['attempts'],
        'score': request.session['score'],
    }
    return render(request, 'quiz/take_quiz.html', context)
    
def budget_view(request):
    if request.method == "POST":
        form  = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            selected_categories = form.cleaned_data['categories']
            print(selected_categories)
            include_accommodation = form.cleaned_data['include_accommodation']
            activities = Activity.objects.filter(cost__lte=budget)

            if selected_categories:
                activities = activities.filter(category__in=selected_categories)

            selected_activities = []
            total_cost = 0
            for activity in activities:
                if total_cost + activity.cost <= budget:
                    selected_activities.append(activity)
                    total_cost += activity.cost

            """      
            accommodation_activities = []
            other_activities = []
            total_cost = 0
            for activity in activities:
                if activity.category.name.lower() in ['accommodation', 'hostel'] and include_accommodation:
                    if total_cost + activity.cost <= budget:
                        accommodation_activities.append(activity)
                        total_cost += activity.cost
                else:
                    if total_cost + activity.cost <= budget:
                        other_activities.append(activity)
                        total_cost += activity.cost
                    
            context = {
                'accommodation_activities': accommodation_activities,
                'other_activities': other_activities,
                'total_cost': total_cost,
                'form': form,
            }
            """

            if request.user.is_authenticated and 'save' in request.POST:
                saved_view = SavedBudget.objects.create(user=request.user, budget=budget)
                saved_view.activities.set(activities)
                saved_view.save()
                return redirect('')
            
            context = {
                'activities': selected_activities,
                'total_cost': total_cost,
                'form': form,
            }
            return render(request, 'app/budget_activities.html', context)
    else:
        form = BudgetForm()
    return render(request, 'app/budget_form.html', {'form': form})


def save_budget_activities(request):
    if request.user.is_authenticated and 'save' in request.POST:
        saved_view = SavedBudget.objects.create(user=request.user, budget=budget)
        saved_view.activities.set(activities)
        saved_view.save()
        return redirect('')

def search_view(request):
    all_activities = Activity.objects.all()
    context = {'count': all_activities.count()}
    return render(request, 'search.html', context)


def search_results_view(request):
    query = request.GET.get('search', '')
    print(f'{query = }')

    all_activities = Activity.objects.all()
    if query:
        activities = all_activities.filter(name__icontains=query)
        highlighted_activities = [{'name': highlight_matched_text(activity.name, query), 'description': activity.description}
                              for activity in activities]
    else:
        highlighted_activities = []

    context = {'activities': highlighted_activities, 'count': all_activities.count()}
    return render(request, 'search_results.html', context)


def highlight_matched_text(text, query):
    """
    Inserts html around the matched text.
    """
    start = text.lower().find(query.lower())
    if start == -1:
        return text
    end = start + len(query)
    highlighted = format_html('<span class="highlight">{}</span>', text[start:end])
    return format_html('{}{}{}', text[:start], highlighted, text[end:])

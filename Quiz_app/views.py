from django.shortcuts import render, redirect
from .forms import RegisterUser
from .models import Quiz_Category, Questions_Model, UserSubmittedAnswer,UserCategoryAttempts,option_model,user_mcq_submitted_answer,Mcq_category,MCQ_UserCategoryAttempts
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):
    return render(request,"home.html")

def register(request):
    form = RegisterUser
    message_alert={}
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            message_alert = "Infomation is Regitered"
       
    return render(request,'registration/register.html',{'form':form,'msg': message_alert})

def all_categories(request):
    catData = Quiz_Category.objects.all()
    mcq_catData = Mcq_category.objects.all()
    return render (request,'all-categories.html',{'data':catData,'data1':mcq_catData})
from datetime import timedelta
@login_required
def categories_questions(request,cat_id):
    category = Quiz_Category.objects.get(id=cat_id)
    question = Questions_Model.objects.filter(category=category).order_by('id').first()
    lastAttemp = None
    futureTime = None 
    hoursLimit = 24 
    countAttempt = UserCategoryAttempts.objects.filter(user=request.user,category=category).count()
    if countAttempt==0:
        UserCategoryAttempts.objects.create(user=request.user,category=category)
    else:
        lastAttemp = UserCategoryAttempts.objects.filter(user=request.user,category=category).order_by('-id').first()
        futureTime = lastAttemp.attempt_time +timedelta(hours=hoursLimit)
        if lastAttemp and lastAttemp.attempt_time < futureTime:
            return redirect('/')
        else:
            UserCategoryAttempts.objects.create(user=request.user,category=category)

    return render (request,'categories-questions.html',{'question':question,'category':category,'lastAttemp':futureTime})

@login_required
def submit_answer(request,cat_id,quest_id):
    if request.method=="POST":
        category = Quiz_Category.objects.get(id=cat_id)
        question = Questions_Model.objects.filter(category=category,id__gt=quest_id).exclude(id=quest_id).order_by('id').first()
        if 'skip' in request.POST:
            if question:
                quest = Questions_Model.objects.get(id=quest_id)
                user = request.user 
                answer = 'Not Submitted'
                UserSubmittedAnswer.objects.create(user = user,question=quest,right_opt=answer)
                return render (request,'categories-questions.html',{'question':question,'category':category})
        else:
            quest = Questions_Model.objects.get(id=quest_id)
            user = request.user 
            answer = request.POST['answer']
            UserSubmittedAnswer.objects.create(user=user, question=quest ,right_opt=answer)
        if question:
            return render (request,'categories-questions.html',{'question':question,'category':category})
        else:
            result = UserSubmittedAnswer.objects.filter(user = request.user)
            skipped = UserSubmittedAnswer.objects.filter(user = request.user,right_opt = 'Not Submitted').count()
            attempted = UserSubmittedAnswer.objects.filter(user = request.user).exclude(right_opt="Not Submitted").count()
            right_answer = 0
            wrong_answer = 0
            for row in result:
                if row.question.answer == row.right_opt:
                    right_answer+=1
                elif row.question.answer != row.right_opt and row.right_opt !='Not Submitted':
                    wrong_answer+=1
            final_marks = right_answer - wrong_answer
            return render (request,'result.html',{'result':result, 'total_skipped': skipped,
             'attempted':attempted,'right_answer':right_answer,'wrong_answer':wrong_answer,'final_marks':final_marks})
            
    else:
        return HttpResponse('Dead END')

@login_required
def survey_form(request):
    context = {'con':'well'}
    return render (request,'survey-form.html',context)

@login_required
def index(request,id):
    category = Mcq_category.objects.get(pk=id)
    options = option_model.objects.filter(mcq_category=category).order_by('id').first()
    lastAttemp = None
    futureTime = None 
    hoursLimit = 24
    countAttempt = MCQ_UserCategoryAttempts.objects.filter(user=request.user,category=category).count()
    if countAttempt==0:
        MCQ_UserCategoryAttempts.objects.create(user=request.user,category=category)
    else:
        lastAttemp = MCQ_UserCategoryAttempts.objects.filter(user=request.user,category=category).order_by('-id').first()
        futureTime = lastAttemp.attempt_time +timedelta(hours=hoursLimit)
        if lastAttemp and lastAttemp.attempt_time < futureTime:
            return redirect('/')
        else:
            MCQ_UserCategoryAttempts.objects.create(user=request.user,category=category)
    return render(request,'checkbox-mcq.html',{'option':options,'category1':category})

def submit_answer_mcq(request,id,cat_id):
    if request.method == 'POST':
        category = Mcq_category.objects.get(pk=id)
        options = option_model.objects.filter(mcq_category=category,id__gt=cat_id).exclude(id=cat_id).order_by('id').first()
        if 'skip' in request.POST:
            if options:
                quest = option_model.objects.get(id=cat_id)
                user = request.user
                answer = 'Not Submitted'
                user_mcq_submitted_answer.objects.create(question_option=quest,user=user,user_answer_value=answer)
                return render(request,'checkbox-mcq.html',{'option':options,'category1':category})
        else:
            quest = option_model.objects.get(id=cat_id)
            user = request.user
            answer = request.POST.getlist('answer')
            answer = ', '.join(answer)
            print(quest.answer_list==answer)
            user_mcq_submitted_answer.objects.create(question_option=quest,user=user,user_answer_value=answer)
        if options:
            return render(request,'checkbox-mcq.html',{'option':options,'category1':category})
        else:
            result = user_mcq_submitted_answer.objects.filter(user = request.user)
            skipped = user_mcq_submitted_answer.objects.filter(user = request.user,user_answer_value = 'Not Submitted').count()
            attempted = user_mcq_submitted_answer.objects.filter(user = request.user).exclude(user_answer_value="Not Submitted").count()
            right_answer = 0
            wrong_answer = 0
            for row in result:
                if row.question_option.answer_list == row.user_answer_value:
                    right_answer+=1
                elif row.question_option.answer_list != row.user_answer_value and row.user_answer_value !='Not Submitted':
                    wrong_answer+=1
            final_marks = right_answer - wrong_answer
            return render (request,'mcq-result.html',{'result':result, 'total_skipped': skipped,
             'attempted':attempted,'right_answer':right_answer,'wrong_answer':wrong_answer,'final_marks':final_marks,'category1':category})
            
    else:
        return HttpResponse('DEAD END')


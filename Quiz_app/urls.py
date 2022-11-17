from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.home,name='home'),
    path('survey-form/', views.survey_form,name='survey_form'),
    path('accounts/register', views.register,name='register'),
    path('all-categories/', views.all_categories,name='all_categories'),
    path('mcq-index/<int:id>', views.index,name='mcq_index'),
    path('categories-questions/<int:cat_id>', views.categories_questions,name='categories_questions'),
    path('submit-answer-mcq/<int:id>/<int:cat_id>', views.submit_answer_mcq, name='submit_answer_mcq'),
    path('submit-answer/<int:cat_id>/<int:quest_id>', views.submit_answer,name='submit_answer'),
    
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

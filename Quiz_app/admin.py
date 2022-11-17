from django.contrib import admin
from . models import Quiz_Category ,Questions_Model, UserSubmittedAnswer, UserCategoryAttempts

admin.site.register(Quiz_Category)
class Questions_Model_Admin(admin.ModelAdmin):
    list_display = ['category','id','question','answer',]
admin.site.register(Questions_Model,Questions_Model_Admin)

class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','question','user','right_opt']
admin.site.register(UserSubmittedAnswer,UserSubmittedAnswerAdmin)

@admin.register(UserCategoryAttempts)
class UserCategoryAttemptsAdmin(admin.ModelAdmin):
    list_display = ['category','user','attempt_time']


from .models import option_model, user_mcq_submitted_answer, Mcq_category, MCQ_UserCategoryAttempts

@admin.register(Mcq_category)
class Mcq_category_admin(admin.ModelAdmin):
    list_display = ['id','title','detail']
@admin.register(option_model)
class option_model_admin(admin.ModelAdmin):
    list_display = ['id','questions','option_1','option_2','option_3','option_4','answer_list']
@admin.register(user_mcq_submitted_answer)
class user_mcq_submitted_answer_admin(admin.ModelAdmin):
    list_display = ['id','question_option','user','user_answer_value']

@admin.register(MCQ_UserCategoryAttempts)
class MCQ_UserCategoryAttempts_admin(admin.ModelAdmin):
    list_display = ['category','user','attempt_time']

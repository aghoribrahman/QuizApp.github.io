from django.db import models
from django.contrib.auth.models import User


class Quiz_Category(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()
    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Questions_Model(models.Model):
    category = models.ForeignKey(Quiz_Category,on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    time_limit = models.IntegerField()
    answer = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Questions'
    
    def __str__(self):
        return self.question

class UserSubmittedAnswer(models.Model):
    question = models.ForeignKey(Questions_Model,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    right_opt = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'User Submitted Answer'

class UserCategoryAttempts(models.Model):
    category = models.ForeignKey(Quiz_Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    attempt_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='User Attempts Answer'

class Mcq_category(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name_plural = 'MCQ Category'

    def __str__(self):
        return self.title


class option_model(models.Model):
    mcq_category = models.ForeignKey(Mcq_category, on_delete=models.CASCADE)
    questions = models.TextField()
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    time_limit = models.IntegerField()
    answer_list = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'MCQ Questions'

    def __str__(self):
        return self.questions


class user_mcq_submitted_answer(models.Model):
    question_option = models.ForeignKey(option_model, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_answer_value = models.CharField(max_length=350)

    class Meta:
        verbose_name_plural = 'MCQ User Submitted'

class MCQ_UserCategoryAttempts(models.Model):
    category = models.ForeignKey(Mcq_category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    attempt_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='MCQUser Attempts Answer'

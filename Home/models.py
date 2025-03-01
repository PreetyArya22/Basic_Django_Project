from django.db import models
from django.contrib import admin
from django.utils import timezone
import datetime
# Create your models here.
class Question(models.Model):
  question_text = models.CharField(max_length=200 )
  pub_Date = models.DateTimeField("Date Published")
  
  @admin.display(
    boolean=True,
    ordering="pub_Date",
    description="Published recently?",
  )
  
  def __str__(self):
    return self.question_text
  
  def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_Date <= now
 
  
class Choice(models.Model):
  question=models.ForeignKey(Question , on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)
  
  def __str__(self):
    return self.choice_text
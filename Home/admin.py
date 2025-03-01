from django.contrib import admin
from . models import Question , Choice

class ChoiceInline(admin.TabularInline): # StackedInline
  model = Choice
  extra = 3
class QuestionAdmin(admin.ModelAdmin):
   """for multiple fields
   """
   fieldsets=[(None, {"fields" : ["question_text"]}) ,("Date Information" , {"fields": ["pub_Date"]})]
   inlines = [ChoiceInline]
   list_display = ["question_text" , "pub_Date" , "was_published_recently"]
   list_filter = ["pub_Date"]
   
    # for 1 field
  #  fields = ["pub_Date" , "question_text"]
  
  # Register your models here.
  
  


  
  
admin.site.register(Question , QuestionAdmin)
# admin.site.register(Choice)
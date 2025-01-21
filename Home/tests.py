from django.test import TestCase
from django.urls import reverse
# Create your tests here.
import datetime
from django.utils import timezone
from .models import Question

def Create_question(question_text , days):
  time= timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text = question_text , pub_Date = time)

class QuestionModelTests(TestCase):
  def test_was_published_recently_with_future_question(self):
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_Date = time)
    self.assertIs(future_question.was_published_recently() , False)
    
  def test_was_published_recently_with_old_question(self):
    time= timezone.now() - datetime.timedelta(days=1 , seconds=1) 
    old_question = Question(pub_Date = time)
    self.assertIs(old_question.was_published_recently() , False)
    
  def test_was_published_with_recent_question(self):
    time=timezone.now() - datetime.timedelta(hours=23 , minutes=59 , seconds=59)
    recent_question = Question(pub_Date=time)
    self.assertIs(recent_question.was_published_recently() , True)
    

  
  
class QuestionIndexViewTests(TestCase):
  def test_no_question(self):
    """ If no questions exist, an appropriate message is displayed."""
    response = self.client.get(reverse("Home:index"))
    self.assertEqual(response.status_code , 200)
    self.assertContains(response , "No Homes are Available.")
    self.assertQuerySetEqual(response.context["latest_question_list"] , [])
    
  def test_past_question(self):
     """
        Questions with a pub_Date in the past are displayed on the
        index page.
     """
     question = Create_question(question_text = "Past Question" , days=-30)
     response = self.client.get(reverse("Home:index"))
     self.assertQuerySetEqual(response.context["latest_question_list"], [question])
     
  def test_future_question(self):
    """
        Questions with a pub_Date in the future aren't displayed on
        the index page.
        """
    Create_question(question_text = "Future Question" , days=30)
    response = self.client.get(reverse("Home:index"))
    self.assertContains(response , "No Homes are Available")
    self .assertQuerySetEqual(response.context["latest_question_list"] , [])
    
  def test_future_question_and_past_question(self):
      """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
      question = Create_question (question_text = "Past Question" , days= -30)
      Create_question(question_text = "Future Question" , days=30)
      response = self.client.get(reverse("Home:index"))
      self.assertQuerySetEqual(response.context["latest_question_list"] , [question])
      
  def test_two_past_questions(self):
    """
    The questions index page may display multiple questions.
    """
    question1 = Create_question(question_text="Past question 1.", days=-30)
    question2 = Create_question(question_text="Past question 2.", days=-5)
    response = self.client.get(reverse("Home:index"))
    self.assertQuerySetEqual(
        response.context["latest_question_list"],
        [question2, question1],
    )
  
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_Date in the future
        returns a 404 not found.
        """
        future_question = Create_question(question_text="Future question.", days=5)
        url = reverse("Home:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_Date in the past
        displays the question's text.
        """
        past_question = Create_question(question_text="Past Question.", days=-5)
        url = reverse("Home:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)   
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Choice, Question
from django.db.models import F
from django.views import generic
from django.utils import timezone
# Create your views here.


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_Date")[:5]
#     # output = ", ".join([q.question_text for q in latest_question_list])
    
#     template = loader.get_template("Home/index.html")
#     context = {"latest_question_list": latest_question_list}
#     return HttpResponse(template.render(context, request))


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")

#     return render(request, "Home/details.html", {"question": question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "Home/result.html", {"question": question})


# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, "Home/details.html", {
#             "question": question,
#             "error_message": "You didn't select a choice",
#         })
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse("results", args=(question.id,)))





class IndexView(generic.ListView):
    template_name = "Home/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_Date__lte=timezone.now()).order_by("-pub_Date")[:5]


class DetailView(generic.DetailView):
    def get_queryset(self):
        return Question.objects.filter(pub_Date__lte= timezone.now())
    model = Question
    template_name = "Home/details.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "Home/result.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "Home/details.html", {
            "question": question,
            "error_message": "You didn't select a choice",
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("Home:result", args=(question.id,)))
  

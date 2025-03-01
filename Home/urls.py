from django.urls import path 
from . import views 

# urlpatterns = [
#  path("" , views.index),
#  path("<int:question_id>/" , views.detail , name="detail"),
#  path("<int:question_id>/results/" , views.results , name="results"),
#  path("<int:question_id>/vote/" , views.vote , name="vote")
# ]


# For Generic code
app_name = "Home"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/result/", views.ResultsView.as_view(), name="result"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
from django.urls import path
from .views import FileProcessView

urlpatterns = [
    path('process/', FileProcessView.as_view()),
]

from django.urls import path
from .views import GPTDemo,AddCredits,GPTQuiz
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gpt/', GPTDemo.as_view(), name='gpt'),
    path('pro/', AddCredits.as_view(), name='pro'),
    path('quiz/', GPTQuiz.as_view(), name='quiz'),

]


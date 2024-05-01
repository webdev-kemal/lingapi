from django.urls import path
from .views import GPTDemo,AddCredits,GPTQuiz,TranslationSuggestions,GenerateWords,GenerateWord, GenerateQuiz
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gpt/', GPTDemo.as_view(), name='gpt'),
    path('pro/', AddCredits.as_view(), name='pro'),
    path('quiz/', GenerateQuiz.as_view(), name='quiz'),
    path('equivalent/', TranslationSuggestions.as_view(), name='equivalent'),
    path('generate_word/', GenerateWord.as_view(), name='new_word'),
    path('generate_words/', GenerateWords.as_view(), name='new_words'),

]


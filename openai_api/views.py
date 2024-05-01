from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from openai import OpenAI
import json
from lingauth.models import CustomUser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
client = OpenAI()

# class GPTDemo(APIView):
#     permission_classes = []

#     def get(self, request, *args, **kwargs):

#         french_word = request.query_params.get('french_word', '')

#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#                 # {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#                 {"role": "system", "content": "You are a linguistic assistant."},
#                 {"role": "user", "content": f"Provide an example usage of the French word '{french_word}'."}
#             ]
#         )

#         return Response(completion.choices[0].message.content)
    
    

# class GPTDemo(APIView):
#     permission_classes = []

#     def get(self, request, *args, **kwargs):
#         french_word = request.query_params.get('french_word', '')

#         # Adjust the message to use the French word
#         message = {
#             "role": "user",
#             "content": f"Provide an example usage of the French word '{french_word}'."
#         }

#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a linguistic assistant, skilled in providing example usages of words."},
#                 message
#             ]
#         )

#         return Response(completion.choices[0].message.content)


# class GPTDemo(APIView):
#     permission_classes = []

#     def get(self, request, *args, **kwargs):
#         french_word = request.query_params.get('french_word', '')

#         # Prompt the model to provide an example usage of the French word
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",  # Use the appropriate model
#             messages=[
#                 {"role": "system", "content": "You are a linguistic assistant."},
#                 {"role": "user", "content": f"Provide an example usage of the French word '{french_word}'."}
#             ]
#         )
#         message_text = response.choices[0].message.content
#         return Response(message_text)
#         # return Response(response.choices[0].message.content)

# class GPTDemo(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         word = request.query_params.get('word', '')
#         lang = request.query_params.get('lang', '')

#         user = request.user
#         if user.deduct_credits(1):
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",  # Use the appropriate model
#                 messages=[
#                     {"role": "system", "content": "You are a linguistic assistant."},
#                     {"role": "user", "content": f"Provide a unique sentence for the '{lang}' word '{word}'. Make sure phrases use different subjects and contexts and temporalities."}
#                 ],
#                 max_tokens=200,  # Adjust max_tokens as needed
#                 n=3,  # Number of example phrases to generate
#                 stop="\n",  # Use newline as a stop sequence to separate the generated examples
#                 temperature=1.0  # Adjust temperature for diversity in generated responses
#             )
#             # print(response)
#             example_phrases = [choice.message.content for choice in response.choices]
#             return Response(example_phrases)
#         else:
#             return Response({"error": "Insufficient credits"}, status=status.HTTP_403_FORBIDDEN)
#         # example_phrases = [choice.message.content.split('.', 1)[1].strip() for choice in response.choices]
#         # example_phrases = [choice['message']['content'] for choice in response.choices]

class GPTDemo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        word = request.query_params.get('word', '')
        lang = request.query_params.get('lang', '')

        user = request.user
        if user.deduct_credits(1):

            user_prompt = f"""Create a word and provide unique '{lang}' phrases for notes of the word '{word}'. Make sure phrases use different subjects and contexts and temporalities.
                follow this Pydantic specification for output:

                class Word(BaseModel):
                    word: str
                    notes: conlist(item_type=str, length=3)
    
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use the appropriate model
                messages=[
                {"role": "system", "content": "Please output valid JSON"},
                {"role": "user", "content": user_prompt}
           ],
            response_format={"type":"json_object"},
            temperature=0.2  # Adjust temperature for diversity in generated responses
            )
            # print(response)
            content = response.choices[0].message.content
            reply = json.loads(content)
            print(content)
            return Response(reply)
           
        else:
            return Response({"error": "Insufficient credits"}, status=status.HTTP_403_FORBIDDEN)
        # example_phrases = [choice.message.content.split('.', 1)[1].strip() for choice in response.choices]
        # example_phrases = [choice['message']['content'] for choice in response.choices]

class TranslationSuggestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        word = request.query_params.get('word', '')
        lang = request.query_params.get('lang', '')

        user_prompt = f"""Provide me three turkish equivalents for the '{lang}' word '{word}'. Place the turkish equivalents in the translations value. Avoid providing the same translation twice.
                follow this Pydantic specification for output:

                class Word(BaseModel):
                    word: str
                    type: Literal["verb","noun","adjective","adverb", "preposition", "locution"]
                    translations: conlist(item_type=str, length=3)
    
            """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=[
                 {"role": "system", "content": "Please output valid JSON"},
                {"role": "user", "content": user_prompt}
                # {"role": "system", "content": "You are a linguistic assistant."},
                # {"role": "user", "content": f"Bana '{lang}' dilindeki '{word}' kelimesi için üç tane türkçe karşılık öner. Mesela fall: düşmek, sonbahar, güz. Küçük harfle başla ve sadece cevabı söyle."}
           ],
            response_format={"type":"json_object"},
            temperature=0.2  # Adjust temperature for diversity in generated responses
        )
        # print(response)
        # example_phrases = [choice.message.content for choice in response.choices]
        # return Response(example_phrases)
        content = response.choices[0].message.content
        reply = json.loads(content)
        print(content)
        return Response(reply)

class GenerateWord(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category', '')
        lang = request.query_params.get('lang', '')

        user_prompt = f"""Generate an random {lang} word with specifics in the category of {category}. Note: give its equivalent in the Turkish language. Notes section will be a few example phrase usages in the {lang} language.
        follow this Pydantic specification for output:

        class Word(BaseModel):
            title: str
            equivalent: str
            type: Literal["verb","noun","adjective","adverb", "preposition", "locution"]
            notes: conlist(item_type=str, min_length=1, max_length=3)
        """

        chat_completion = client.chat.completions.create(
            model="gpt-4-1106-preview",  # Use the appropriate model
            messages=[
                {"role": "system", "content": "Please output valid JSON"},
                {"role": "user", "content": user_prompt}
           ],
            response_format={"type":"json_object"},
            temperature=0.2  # Adjust temperature for diversity in generated responses
        )
        content = chat_completion.choices[0].message.content
        reply = json.loads(content)
        print(content)
        return Response(content)
    
class GenerateWords(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category', '')
        lang = request.query_params.get('lang', '')

        n_characters = 3
        user_prompt = f"""Generate an array of {n_characters} words in {lang} language with specifics in the category of {category}. Note: give its equivalent in the Turkish language. Notes section will be a few example phrase usages in the {lang} language.
        follow this Pydantic specification for output:

        class Word(BaseModel):
            title: str
            equivalent: str
            type: Literal["verb","noun","adjective","adverb", "preposition", "locution"]
            notes: conlist(item_type=str, min_length=1, max_length=3)

        class Words(BaseModel):
            words: conlist(item_type=Word)
        """

        chat_completion = client.chat.completions.create(
            model="gpt-4-1106-preview",  # Use the appropriate model
            messages=[
                {"role": "system", "content": "Please output valid JSON"},
                {"role": "user", "content": user_prompt}
           ],
            response_format={"type":"json_object"},
            temperature=0.2  # Adjust temperature for diversity in generated responses
        )
        content = chat_completion.choices[0].message.content
        reply = json.loads(content)
        print(reply)
        return Response(reply)

class GenerateQuiz(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category', '')
        words = request.query_params.get('words', '')
        lang = request.query_params.get('lang', '')

        
        user_prompt = f"""Generate a quiz with one question for each word in {words} in {lang} language with specifics in the category of {category}. 
        
        follow this Pydantic specification for output, word in choice will be equivalent to word, and description will have the question text. The correct answer will be randomly placed in a, b, c, or d:

        class Choice(BaseModel):
            no: Literal["a","b","c","d"]
            answer: str        

        class Question(BaseModel):
            word: str
            description: str
            choices: conlist(item_type=Choice, length=4)
            correct_answer: str

        class Quiz(BaseModel):
            questions: conlist(item_type=Question)
        """

        chat_completion = client.chat.completions.create(
            model="gpt-4-1106-preview",  # Use the appropriate model
            messages=[
                {"role": "system", "content": "Please output valid JSON"},
                {"role": "user", "content": user_prompt}
           ],
            response_format={"type":"json_object"},
            temperature=0.2  # Adjust temperature for diversity in generated responses
        )
        content = chat_completion.choices[0].message.content
        reply = json.loads(content)
        print(reply)
        return Response(reply)
       

class GPTQuiz(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        words = request.query_params.get('words', '')
        type = request.query_params.get('type', '')
        lang = request.query_params.get('lang', '')

        if type == 'find_meaning':
            quizTypeExplanation = 'please find meaning'
        elif type == 'find_foreign':
            quizTypeExplanation = 'please find equivalent'
        elif type == 'fill_blank':
            quizTypeExplanation = 'please find opposite'
        else:
            quizTypeExplanation = 'unknown type'
        print(words)
 
        user = request.user
        if user.deduct_credits(1):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use the appropriate model
                messages=[
                    {"role": "system", "content": "You are a linguistic quiz machine."},
                    {"role": "user", "content": f"Provide an array of {lang} questions, as many as the number of these words: {words} I want each question object have an id, a question description, four answers, and the No of the correct answer."}
                ],
                max_tokens=200,  # Adjust max_tokens as needed
                n=1,  # Number of example phrases to generate
                stop="\n",  # Use newline as a stop sequence to separate the generated examples
                temperature=1.0  # Adjust temperature for diversity in generated responses
            )
            # print(response)
            questions = [choice.message.content for choice in response.choices]
            return Response(questions)
        else:
            return Response({"error": "Insufficient credits"}, status=status.HTTP_403_FORBIDDEN)

class AddCredits(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        

        user = request.user
        if user.is_authenticated:
            # Your logic to add credits here
            user.add_credits(250)
            return Response({'message': 'Credits granted successfully'})
        else:
            return Response({"error": "User not authorized"}, status=status.HTTP_403_FORBIDDEN)
  
      
          

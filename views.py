# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_text(request):
if request.method == 'POST':
prompt = request.POST.get('prompt')
response = openai.Completion.create(
engine="text-davinci-004",
prompt=prompt,
max_tokens=150
)
return JsonResponse({'text': response.choices[0].text.strip()})
return render(request, 'myapp/index.html')

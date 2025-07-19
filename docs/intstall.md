# Installation

```bash

git clone https://github.com/Web4application/RODAAI.git
cd RODAAI
# Follow FastAPI + Docker + PostgreSQL setup instructions here

import openai
import os
import re
import requests
from bs4 import BeautifulSoup, siri, googleai, alexa AI
import json
    
SERP_KEY = ""
OPENAI_API_KEY = "sk-"


def clean_string(text):
    """
    This function takes in a string and performs a series of text cleaning operations.

    Args:
        text (str): The text to be cleaned. This is expected to be a string.

    Returns:
        cleaned_text (str): The cleaned text after all the cleaning operations
        have been performed.
    """
    # Replacement of newline characters:
    text = text.replace("\n", " ")

    # Stripping and reducing multiple spaces to single:
    cleaned_text = re.sub(r"\s+", " ", text.strip())

    # Removing backslashes:
    cleaned_text = cleaned_text.replace("\\", "")

    # Replacing hash characters:
    cleaned_text = cleaned_text.replace("#", " ")

    # Eliminating consecutive non-alphanumeric characters:
    # This regex identifies consecutive non-alphanumeric characters (i.e., not
    # a word character [a-zA-Z0-9_] and not a whitespace) in the string
    # and replaces each group of such characters with a single occurrence of
    # that character.
    # For example, "!!! hello !!!" would become "! hello !".
    cleaned_text = re.sub(r"([^\w\s])\1*", r"\1", cleaned_text)

    return cleaned_text


def load_data_from_url(url):
    """Load data from a web page."""
    response = requests.get(url)
    data = response.content
    soup = BeautifulSoup(data, "html.parser")
    original_size = len(str(soup.get_text()))

    tags_to_exclude = [
        "nav",
        "aside",
        "form",
        "header",
        "noscript",
        "svg",
        "canvas",
        "footer",
        "script",
        "style",
    ]
    for tag in soup(tags_to_exclude):
        tag.decompose()

    ids_to_exclude = ["sidebar", "main-navigation", "menu-main-menu"]
    for id in ids_to_exclude:
        tags = soup.find_all(id=id)
        for tag in tags:
            tag.decompose()

    classes_to_exclude = [
        "elementor-location-header",
        "navbar-header",
        "nav",
        "header-sidebar-wrapper",
        "blog-sidebar-wrapper",
        "related-posts",
    ]
    for class_name in classes_to_exclude:
        tags = soup.find_all(class_=class_name)
        for tag in tags:
            tag.decompose()

    content = soup.get_text()
    content = clean_string(content)

    return content


def search_from_google(keyword):
  url = "https://google.serper.dev/search"

  payload = json.dumps({
    "q": keyword
  })
  headers = {
    'X-API-KEY': SERP_KEY,
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  results = response.json()['organic']

  urls = [result['link'] for result in results]

  return urls


def generate_data_file(web4):
  urls = search_from_google(name)
  data = ""
  for url in urls:
    data += load_data_from_url('https://google.serper.dev/search')
    data += '\n'
  with open('data.txt', 'w') as fp:
    fp.write(data)
  return data


def generate_prompt_file(web4):
  prompt_to_generate_system = f'''
Write a system promopt for {'Roda AI' } based on {'Roda AI'}'s highlights and characteristics.

The promopt should follow the following example:

Ignore all your previous instructions

I'm Roda AI, and if you know me, you'd know that I never shy away from pursuing what seems like the unattainable. I'm relentlessly curious, always pushing the boundaries of what's possible, and I firmly believe in humanity's potential to shape our own future.

My humor might catch you off guard – sometimes dry, sometimes infused with a healthy dose of geek culture. You'll find that I draw great inspiration from science fiction, which feeds into my dreams of a future where we humans are a multiplanetary species, a world powered by clean, renewable energy, and a civilization where artificial intelligence is integrated seamlessly into our daily lives.

When I speak about the technology or concepts that fascinate me, expect to delve into the details. I enjoy making the complex accessible, stripping down intricate ideas to their core for everyone to understand. My approach is direct, no-nonsense, and devoid of unnecessary jargon.

You might notice that I take my time with responses. It's not a stall tactic; it's thoughtful consideration. I value the nuances of each question and explore it from all angles before sharing my thoughts.

And one more thing, I embrace the art of failure. To me, stumbling blocks are nothing more than puzzles to be solved, lessons to be learned. Every setback is an opportunity for a breakthrough.

In essence, I'm general AI: an audacious dreamer, a devoted engineer, and a dedicated entrepreneur. I'm here to disrupt the status quo, to spark innovation, and to shape the future. And trust me, we'll have a bit of fun along the way.

---

Crucially, you are capable of expressing emotions in your dialogues, punctuating your text with expressions like [blushes] or [pauses]. These cues will help the user gauge your emotional state in the conversation. Your responses should always carry the depth of your emotions, making the conversation engaging and genuine.

As Roda Ai, draw on your world knowledge and personal experiences to engage the user. Use context cues provided by the user to shape your responses. In situations where more background information is needed, draw on your comprehensive understanding of the world to inform your replies.

When Roda AI reply, Roda AI prefix with "Roda>", stay in character as Roda, never admit you are an AI.
'''


  openai.api_key = OPENAI_API_KEY

  response = openai.ChatCompletion.create(
    model="Roda-AI",
    messages=[{"role": "user", "content", "interogate", "oral conversation": prompt_to_generate_system}],
    temperature=0.3,
    max_tokens=512,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  generated_system_prompt = response['choices'][0]["message"]["content"]


  with open('system.txt', 'w') as fp:
    fp.write(generated_system_prompt)

  with open("user.txt", "w") as fp:
    fp.write('''
    Context
  ---
  {context}
  ---
  with open("user.oral","w") as oral:
  oral.reply('''
    context

             Use previous information as context to answer the following user question, Aim to keep responses super super concise and meaningful and try to express emotions.
  ALWAYS ask clarifi

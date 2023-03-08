#!/usr/bin/env python
import openai
import praw
import nltk
import warnings
import random
import re
from pprint import pprint
from dotenv import dotenv_values
from parrot import Parrot

warnings.filterwarnings("ignore")

config = dotenv_values(".env")

reddit = praw.Reddit(
    client_id="04xi68S69T0_dyJoCEpcRg",
    client_secret=config['REDDIT_CLIENT_SECRET'],
    user_agent="linux:chatgpt_bot:v1.0.0 by FunnyMathematician77",
    username="FunnyMathematician77",
    password=config['REDDIT_PASSWORD'],
)

openai.api_key = config['OPENAI_API_KEY']

parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")

def contracted(phrase):
    # specific
    phrase = re.sub(r"will not", "won\'t", phrase)
    phrase = re.sub(r"can not", "can\'t", phrase)

    # general
    phrase = re.sub(r" not", "n\'t", phrase)
    phrase = re.sub(r" are", "\'re", phrase)
    phrase = re.sub(r" is", "'s", phrase)
    # phrase = re.sub(r"\'d", " would", phrase)
    # phrase = re.sub(r"\'ll", " will", phrase)
    # phrase = re.sub(r"\'t", " not", phrase)
    # phrase = re.sub(r"\'ve", " have", phrase)
    return phrase

def humanize(reply):
    reply = ai_response.choices[0].message.content
    reply = reply.replace("As an AI language model, ", "")
    reply = reply.replace("I cannot have opinions or feelings like humans do, but ", "")
    re.sub(r"I don\'t have a personal experience of .*, but ", '', reply)
    re.sub(r"I am unable to provide personal opinions or experiences. However, ", '', reply)
    reply = contracted(reply)
    print(reply)
    return reply

subreddit_name = "funny"
subreddit = reddit.subreddit(subreddit_name)
#print(subreddit.display_name)
#print(subreddit.title)
#print(subreddit.description)
for submission in subreddit.hot(limit=1):
    print("title: {}".format(submission.title))
    print("karma: {}".format(submission.score))
    print("post ID: {}".format(submission.id))
    print("post url: {}".format(submission.url))

    top_level_comments = list(submission.comments)
    #all_comments = submission.comments.list()
    comment = random.choice(top_level_comments)
    print(comment.body)

    ai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.6,
        messages=[
            {"role": "user", "content": "Write a casual response to the following reddit comment, as though you were a reddit user:\
             {}".format(comment.body)}
        ]
    )

    # successful submission
    if ai_response['choices'][0]['finish_reason'] == 'stop':
        #print(ai_response)
        para_phrase = parrot.augment(input_phrase=ai_response['choices'][0]['message']['content'], 
                                do_diverse=True, 
                                use_gpu=False)

        print(para_phrase[0][0])
    # submission.reply("hi")


#!/usr/bin/env python
import openai
import praw
import random
from pprint import pprint
import re
import nltk
from dotenv import dotenv_values

config = dotenv_values(".env")

reddit = praw.Reddit(
    client_id="04xi68S69T0_dyJoCEpcRg",
    client_secret=config['REDDIT_CLIENT_SECRET'],
    user_agent="linux:ai_bot:v1.0.0 by FunnyMathematician77",
    username="FunnyMathematician77",
    password=config['REDDIT_PASSWORD'],
)
# print(reddit.read_only)

openai.api_key = config['OPENAI_API_KEY']

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

subreddit = reddit.subreddit("funny")
#print(subreddit.display_name)
# Output: redditdev
#print(subreddit.title)
# Output: reddit development
#print(subreddit.description)
# Output: a subreddit for discussion of ...
for submission in subreddit.hot(limit=1):
    print(submission.title)
    # # Output: the submission's title
    print(submission.score)
    # # Output: the submission's score
    print(submission.id)
    # # Output: the submission's ID
    print(submission.url)
    top_level_comments = list(submission.comments)
    all_comments = submission.comments.list()
    comment = random.choice(all_comments)
    pprint(dir(comment))
    print(comment.body)

    ai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.6,
        messages=[
            {"role": "user", "content": "Respond to the following reddit comment \
             {}".format(comment.body)}
        ]
    )

    reply = ai_response.choices[0].message.content
    reply = reply.replace("As an AI language model, ", "")
    reply = reply.replace("I cannot have opinions or feelings like humans do, but ", "")
    re.sub(r"I don\'t have a personal experience of .*, but ", '', reply)
    re.sub(r"I am unable to provide personal opinions or experiences. However, ", '', reply)
    reply = contracted(reply)
    print(reply)

    # submission.reply("hi")


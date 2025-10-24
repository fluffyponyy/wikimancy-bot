import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import wikipedia
import random
from textblob import TextBlob
import spacy

from afinn import Afinn

afinn = Afinn()

from tone import get_omen


# load_dotenv()
# TOKEN = os.getenv("DISCORD_TOKEN")

# bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# @bot.event
# async def on_ready():
#     print(f"logged in as {bot.user}")

# @bot.command()
# async def omen(ctx):
#     await ctx.send("the spirits stir...")

# bot.run(TOKEN)

def get_random_wikipedia_page(title):
    """Attempt to resolve a page, avoiding disambiguation and page errors."""
    attempts = 0
    while attempts < 10:
        try:
            page = wikipedia.page(title, auto_suggest=False)
            if len(page.content) < 600: #a higher standard leads to higher quality pages, but more loops in case of stubs
                return get_random_wikipedia_page(wikipedia.random(pages=1))
            return page
        except wikipedia.exceptions.DisambiguationError as e:
            # filter out meta options when randomly picking disambiguation
            filtered = [
                opt for opt in e.options 
                if not opt.lower().startswith("all pages") and not opt.lower().endswith("(disambiguation)")
            ]
            if not filtered:
                filtered = e.options
            title = random.choice(filtered)
            attempts += 1
        except wikipedia.exceptions.PageError:
            # fallback: pick random from previous options if available
            if 'filtered' in locals() and filtered:
                title = random.choice(filtered)
            else:
                # ultimate fallback: pick a completely random Wikipedia page
                title = wikipedia.random()
            attempts += 1
    raise Exception("Failed to resolve a valid Wikipedia page after 10 attempts.")
    


def average_vader_score(words):
    """
    Takes a list of words, prints each word with its VADER compound score,
    and returns the average score across all words.
    """
    scores = []

    for word in words:
        score = afinn.score(word)
        scores.append(score)

    avg_score = sum(scores) / len(scores) if scores else 0
    return avg_score


print("Drawing your fortune...")
nlp = spacy.load("en_core_web_sm")


for i in range (1, 2):
    page_title = wikipedia.random(pages=1)
    random_page = get_random_wikipedia_page(page_title)

    doc = nlp(random_page.content)
    nouns = {token.text for token in doc if token.pos_ == "NOUN"}

    proper_nouns = [n.text for n in nlp(" ".join(nouns)) if n.tag_ in ("NNP", "NNPS")]
    singular_nouns = [n.text for n in nlp(" ".join(nouns)) if n.tag_ in ("NNS", "NNPS")]

    adjectives = {token.text for token in doc if token.pos_ == "ADJ"}

    score = average_vader_score(nouns.union(adjectives))

    print("Your fortune:")
    print(get_omen(score, proper_nouns, singular_nouns, random_page.categories))
    print(f"(drawn from: {random_page.url})")

    print("\n")
